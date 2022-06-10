<template>
  <CodeEditor
    v-model="value"
    theme="light"
    width="auto"
    class="my-4"
    :read_only="true"
    :languages="[['python', 'Python']]"
  />
</template>

<script>
import { defineComponent, computed } from '@nuxtjs/composition-api'
import { useDashboardParameters } from '../store'

const template = `# Copyright (c) 2022 Boston Dynamics, Inc.  All rights reserved.

import argparse
import sys
import time
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry

from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand


def hello_spot(config):
    sdk = bosdyn.client.create_standard_sdk('HelloSpotClient')
    robot = sdk.create_robot(config.hostname)
    bosdyn.client.util.authenticate(robot)
    robot.time_sync.wait_for_sync()
    lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    with bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        robot.logger.info("Powering on robot... This may take several seconds.")
        robot.power_on(timeout_sec=20)
        assert robot.is_powered_on(), "Robot power on failed."
        robot.logger.info("Robot powered on.")
        robot.logger.info("Commanding robot to stand...")
        command_client = robot.ensure_client(RobotCommandClient.default_service_name)
        blocking_stand(command_client, timeout_sec=10)
        robot.logger.info("Robot standing.")
        time.sleep(3)
        footprint_R_body = bosdyn.geometry.EulerZXY(yaw=0.4, roll=0.0, pitch=0.0)
        cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
        command_client.robot_command(cmd)
        robot.logger.info("Robot standing twisted.")
        time.sleep(3)
        cmd = RobotCommandBuilder.synchro_stand_command(body_height=0.1)
        command_client.robot_command(cmd)
        robot.logger.info("Robot standing tall.")
        time.sleep(3)
        robot.power_off(cut_immediately=False, timeout_sec=20)
        robot.logger.info("Robot safely powered off.")


def main(argv):
    """Command line interface."""
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    options = parser.parse_args(argv)
    hello_spot(options)


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)

`

export default defineComponent({
  setup () {
    const dashboardParameters = useDashboardParameters()
    return {
      value: computed(() => {
        if (!dashboardParameters.codeSampleParameter) { return '# Code sample will appear here' }
        return template
      })
    }
  }
})

</script>

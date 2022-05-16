import robonomicsinterface as RI

interface = RI.RobonomicsInterface()
num_dt = interface.custom_chainstate("DigitalTwin", "Total")
print("Total number of DigitalTwins:", num_dt)
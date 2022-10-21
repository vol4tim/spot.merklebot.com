<template>
  <div>
    <div v-if="!surveyCompleted">
      <Survey :survey="survey" />
    </div>
    <div v-if="surveyCompleted">
      <p>
        Thank you.
      </p>
    </div>
  </div>
</template>

<script>
import 'survey-core/survey.min.css'
import { StylesManager, Model } from 'survey-core'
import { Survey } from 'survey-vue-ui'

StylesManager.applyTheme('stone')

const surveyJson = {
  title: '',
  description: '',
  logoPosition: 'right',
  pages: [
    {
      name: 'page1',
      elements: [
        {
          type: 'radiogroup',
          name: 'role',
          title: 'Are you representing a company or have personal interest in Web3 for robotics?',
          choices: [
            {
              value: 'individual',
              text: 'Individual'
            },
            {
              value: 'company',
              text: 'Company'
            }
          ],
          isRequired: true
        },
        {
          type: 'text',
          name: 'email',
          inputType: 'email',
          title: 'Your email?',
          isRequired: true
        },
        {
          type: 'html',
          name: '',
          html: '<div class="text-xs italic">* we never store your email and wallet info together, we’ll use your email to send you info about Web3 and robotics. </div>'

        }
      ]
    }
  ]
}

export default {
  name: 'UserInfoSurvey',
  components: {
    Survey
  },
  emits: ['submit'],
  data () {
    const survey = new Model(surveyJson)
    survey.focusFirstQuestionAutomatic = false

    survey.onComplete.add(this.onCompleteSurvey)

    return {
      survey,
      surveyCompleted: false
    }
  },
  methods: {
    onCompleteSurvey (sender) {
      this.$emit('submit', sender.data)
      // alert(results)
      this.surveyCompleted = true
    }
  }
}
</script>

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
  title: 'Please let us know more about you',
  description: "We are asking order to understand our auditory better. After submission of the survey you will get a free ticket and a little amount of XRT to launch Spot robot. All the data provided will be associated with email only. We don't use and never store any association of the data collected with the account address provided.",
  logoPosition: 'right',
  pages: [
    {
      name: 'page1',
      elements: [
        {
          type: 'text',
          name: 'question1',
          title: 'Can we get your email?',
          isRequired: true
        },
        {
          type: 'checkbox',
          name: 'question2',
          title: 'What role sounds closer to you?',
          isRequired: true,
          choices: [
            {
              value: 'item1',
              text: 'Casual web3 user'
            },
            {
              value: 'item2',
              text: 'Web3 early adopter'
            },
            {
              value: 'item3',
              text: 'Developer'
            }
          ],
          hasOther: true
        },
        {
          type: 'boolean',
          name: 'question3',
          title: 'Can we send you our news and updates by email?',
          isRequired: true
        },
        {
          type: 'text',
          name: 'question4',
          title: 'Your Robonomics Network parachain account address (we will send XRTs to it to launch Spot robot demo)?',
          isRequired: true
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
      const results = JSON.stringify(sender.data)
      alert(results)
      this.surveyCompleted = true
    }
  }
}
</script>

<template>
  <b-container fluid="lg">
    <b-row>
      <b-col lg="12" order-lg="2">

        <b-form-row >
          <b-col lg="6" offset-lg="3">
            <template v-if="this.$route.params.shareId">
              <call-display v-bind:called-url="share_link" v-bind:method="response.method" ></call-display>
            </template>
            <template v-else>
              <url-caller v-bind="response" v-on:call-url="getResponse"></url-caller>
            </template>
          </b-col>
        </b-form-row>
      </b-col>
      <b-col lg="12" order-lg="1">
        <b-row >
          <b-col class="text-center stronger-info">
            {{final_status}}
          </b-col>
        </b-row>
        <b-row >
          <b-col class="text-center" lg="6" offset-lg="3">
            {{final_message}}
          </b-col>
        </b-row>
      </b-col>
      <b-col lg="12" order="3">
        <b-row class="text-left p-4 result-row" >
          <b-col lg="3" v-if="response.status">
            <ul class="main-result-box">
              <li class="result-title">URL INFO</li>
              <li>
                <ul class="result-element-section">
                  <li class="result-element-title">DOMAIN</li>
                  <li class="result-element">{{this.response.domain}}</li>
                </ul>
              </li>
              <li>
                <ul class="result-element-section">
                  <li class="result-element-title">SCHEME</li>
                  <li class="result-element">{{this.response.schema}}</li>
                </ul>
              </li>
              <li>
                <ul class="result-element-section">
                  <li class="result-element-title">PATH</li>
                  <li class="result-element">{{this.response.path}}</li>
                </ul>
              </li>
            </ul>
          </b-col>
          <b-col lg="3" v-for="(item,index) in response.call_results" v-bind:key="item.status_code" >
            <ul class="result-box">
              <li class="result-title">RESPONSE</li>
              <li class="result-detail">{{ item.status_code }}</li>
              <li class="result-detail"
                  v-if="response.date && (index === response.call_results.length - 1) ">
                date: {{response.date}}
              </li>
              <li class="result-detail" v-if="item.location">Location: {{item.location}}</li>
              <li class="result-detail" v-if="item.server">Server: {{item.server}}</li>
            </ul>
          </b-col>
        </b-row>
      </b-col>
      <b-col lg="12" order="4" class="mx-auto">
        <b-row >
          <b-col v-if="response.status">
          <b-row>
          <b-col  class="text-center strong-info">
            SHARE
          </b-col>
          </b-row>
            <b-row>
              <b-col  v-if="this.$route.params.shareId">
                <b-col lg="5"  class="mx-auto btn btn-secondary disabled no-hand"> {{this.share_link}} </b-col>
              </b-col>
              <b-col  lg="5" class="mx-auto" v-else>
                <router-link   class="btn btn-secondary fill-col" v-bind:to="'/' + this.shareId" >
                  {{this.share_link}}
                </router-link>
              </b-col>

            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  import axios from 'axios'
  import UrlCaller from './UrlCaller.vue'
  import CallDisplay from './CallDisplay.vue'

  export default {
    name: 'HelloWorld',
    components: {
      UrlCaller,
      CallDisplay
    },
    data () {
      return {
        final_status: '',
        final_message: '',
        response: {},
        share_link: '',
        shareId: ''
      }
    },
    mounted () {
      this.shareId = this.$route.params.shareId
      if (this.shareId) this.getSharedData(this.shareId)
    },
    methods: {
      getResponse (result) {
        this.response = result.data.result
        this.final_status = result.status
        this.final_message = (result.final_message || result.data.result.status_msg)

        this.shareId = this.response.share_id
        this.share_link = window.location.host + '/' + this.shareId
      },
      getSharedData (shareId) {
        axios({
          method: 'GET',
          'url': 'http://localhost:5000/api/v1.0/share/' + shareId,
          'headers': {'content-type': 'application/json'}
        }).then(result => {
          this.getResponse(result)
        }).catch(error => {
          console.log(error)
          if (error.response) {
            this.getResponse(error.response)
            this.final_message = JSON.parse(error.response.data.result.errors).error
          } else if (error.hasOwnProperty('message')) {
            this.final_message = error.message
          }
          this.inSharePage = false
        })

        console.log('shareId: ' + shareId)
      }
    }
  }
</script>

<style lang="scss">
  textarea {
    width: 600px;
    height: 200px;
  }

  .rounded_box {
    border: 1px solid #f6f6f6;
    border-radius: .25rem
  }

  .slight-indent {
    padding: 0 0 2px 5px;
  }

  $box-light-color: #f6f6f6;
  .result-box {
    @extend .rounded_box;
    min-height: 400px;
  }

  .main-result-box {
    @extend .result-box;
    background: $box-light-color;
  }

  .result-detail {
    padding: 10px 0 10px 5px;
    background: $box-light-color;
    margin-bottom: 1px;
  }

  .result_element {
    font-size: 0.9em;
  }

  .text-dark {
    font-weight: bold;
  }

  .result-title {
    @extend .slight-indent;
    font-size: 1.1em;
    padding-bottom: 20px;
  }

  .strong-info {
    font-size: 2em;
    font-weight: bold;
  }
  .stronger-info {
    font-size: 2.5em;
    font-weight: bold;
  }

  .result-element-title {
    @extend .text-dark;
  }

  .result-element-section {
    background-color: #e9e9e9;
    @extend .slight-indent
  }

  body {
    font-size: 14px;
    font-family: Arial, sans-serif;
  }

  ul {
    padding: 0;
    list-style: none;
  }

  ul li {
    display: block;
    padding: 0 0 2px 0px;
    text-decoration: none;
  }
  .no-hand{
    cursor: default;
  }
  .fill-col{
    width: 100%;
  }

</style>

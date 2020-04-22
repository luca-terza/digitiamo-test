<template>
  <b-container>
    <b-row>
      <b-col class="text-center">
        <h1> {{final_status}}</h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="6" offset="3" class="text-center">
        {{final_message}}
      </b-col>
    </b-row>
    <b-form-row>
      <b-col offset="3" cols="6">
        <b-input-group class="border rounded p-4">
          <template v-slot:prepend>
            <b-form-select :options="methods" size="sm" v-model="input.method" variant="info"></b-form-select>
          </template>
          <b-form-input placeholder='url' size="sm" type='text' v-model='input.url'></b-form-input>

          <b-input-group-append>
            <b-button size="sm" text="Button" v-on:click='sendData()' variant="success">Send</b-button>
          </b-input-group-append>
        </b-input-group>
      </b-col>
    </b-form-row>

    <b-row  offset class="text-left p-4 result-row" >
        <b-col cols="3"  v-if="response.status">
          <ul class="main-result-box">
            <li class="result-title">URL INFO</li>
            <li >
              <ul class="result-element-section">
                <li class="result-element-title">DOMAIN</li>
                <li class="result-element">{{this.response.domain}}</li>
              </ul>
            </li>
            <li >
              <ul class="result-element-section">
                <li class="result-element-title">SCHEME</li>
                <li class="result-element">{{this.response.scheme}}</li>
              </ul>
            </li>
            <li >
              <ul class="result-element-section">
                <li class="result-element-title">PATH</li>
                <li class="result-element">{{this.response.path}}</li>
              </ul>
            </li>
          </ul>
        </b-col>
        <b-col v-for="response in response.call_results" v-bind:key="response.status" cols="3" >
          <ul class="result-box">
            <li class="result-title">RESPONSE</li>
            <li class="result-detail" v-if="response.date">date: {{response.date}}</li>
            <li class="result-detail">{{ response.status_code }}</li>
            <li class="result-detail" v-if="response.location">Location: {{response.location}}</li>
            <li class="result-detail" v-if="response.server">Server: {{response.server}}</li>
          </ul>
        </b-col>
    </b-row>

    <b-row>
      <b-col >
        <label>
          <b-textarea cols="90" v-model='response_debug'/>
        </label>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'HelloWorld',
    data () {
      return {
        methods: [
          'GET', 'POST'],
        final_status: '',
        final_message: '',
        input: {
          method: 'GET',
          url: ''
        },
        response_debug: '',
        response: {'status': 'debug'}
      }
    },
    mounted () {
    },
    methods: {
      getResult (result) {
        this.response = result.data.result
        this.response_debug = JSON.stringify(this.response).replace(/,/g, '\n')
        this.final_status = result.status
        this.final_message = this.response.status_msg
      },
      sendData () {
        axios({
          method: 'POST',
          'url': 'http://localhost:5000/api/v1.0/request_url/' + this.input.method,
          'data': {'requested_url': this.input.url},
          'headers': {'content-type': 'application/json'}
        }).then(result => {
          this.getResult(result)
        }).catch(error => {
          console.log(error)
          if (error.response) {
            this.getResult(error.response)
          } else if (error.hasOwnProperty('message')) {
            this.final_message = error.message
          }
        })
      }
    }
  }
</script>

<style lang="scss">
  textarea {
    width: 600px;
    height: 200px;
  }
  .rounded_box{
    border: 1px solid #f6f6f6;
    border-radius:.25rem
  }
  .slight-indent{
    padding: 0 0 2px 5px;
  }

  $box-light-color: #f6f6f6;
  .result-box{
    @extend .rounded_box;
    min-height: 400px;
    padding: 0 0 0 0;
  }
  .main-result-box{
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
  .text-dark{
    font-weight: bold;
  }
  .result-title {
    @extend .slight-indent;
    font-size: 1.1em;
    padding-bottom: 20px;
  }
  .result-element-title {
    @extend .text-dark;
  }
  .result-element-section {
    background-color: #e9e9e9;
    @extend .slight-indent
  }

  body{
    font-size: 14px;
    font-family: Arial,sans-serif;
  }
  ul {
    padding: 0;
    list-style: none;
  }
  ul li {
    display: block;
    padding: 0 0 2px 0px ;
    text-decoration: none;
  }

</style>

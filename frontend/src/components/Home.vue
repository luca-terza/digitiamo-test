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

    <b-row  offset class="text-left p-4" v-if="response != ''">
        <b-col cols="3" class="border rounded">
          <ul>
            <li class="text-dark url-info-title">
                <b-col >URL INFO</b-col>

            </li>
            <li class="text-dark url-info-section-title">
              <b-row>
                <b-col >DOMAIN</b-col>
              </b-row>
              <b-row>
                <b-col>{{this.response.domain}}</b-col>
              </b-row>
            </li>
            <li class="text-dark url-info-section-title">
              <b-row>
                <b-col >SCHEME</b-col>
              </b-row>
              <b-row>
                <b-col>{{this.response.scheme}}</b-col>
              </b-row>
            </li>
            <li class="text-dark url-info-section-title">
              <b-row>
                <b-col >PATH</b-col>
              </b-row>
              <b-row>
                <b-col>{{this.response.path}}</b-col>
              </b-row>
            </li>
          </ul>
        </b-col>
        <b-col v-for="response in this.response.call_results" v-bind:key="response.status_code" cols="3" class="border rounded p-1">
          <ul >
            <li>RESPONSE</li>
            <li v-if="response.date">date: {{response.date}}</li>
            <li >{{ response.status_code }}</li>
            <li v-if="response.location">Location: {{response.location}}</li>
            <li v-if="response.server">Server: {{response.server}}</li>
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
        response: {}
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

<style >
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }

  textarea {
    width: 600px;
    height: 200px;
  }
  .url-info-section-title {
    background-color: lightgray;
    padding-bottom: 2px;
    margin-bottom: 2px;
  }
</style>

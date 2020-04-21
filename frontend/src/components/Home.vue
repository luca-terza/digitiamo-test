<template>
  <b-container>
    <b-row>
      <b-col class="text-center"  >
        <h1> {{final_status}}</h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="6" offset="3" class="text-center">
        {{final_message}}
      </b-col>
    </b-row>
    <b-form-row >
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

    <b-row class="text-center">
    <b-col class="p-4" cols="8" offset="2">
      <b-row>
        <b-col class="border rounded p-1">1 of 3</b-col>
        <b-col class="border rounded p-1">2 of 3 (wider)</b-col>
        <b-col class="border rounded p-1">3 of 3</b-col>
      </b-row>
    </b-col>
    </b-row>

    <b-row >
      <b-col offset="3" cols="6">
        <label>
          <b-textarea v-model='response'/>
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
        response: ''
      }
    },
    mounted () {
    },
    methods: {
      getResult (result) {
        this.response = JSON.stringify(result.data).replace(/,/g, '\n')
        this.final_status = result.status
      },
      sendData () {
        axios({
          method: 'POST',
          'url': 'http://localhost:5000/api/v1.0/request_url/' + this.input.method,
          'data': {'requested_url': this.input.url},
          'headers': {'content-type': 'application/json'}
        }).then(result => {
          this.getResult(result)
          this.final_message = result.statusText
        }).catch(error => {
          console.log(error)
          if (error.response) {
            let result = error.response
            this.getResult(result)
            this.final_message = JSON.parse(result.data.result.errors).error
          } else if (error.hasOwnProperty('message')) {
            this.final_message = error.message
          }
        })
      }
    }
  }
</script>

<style scoped>
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
</style>

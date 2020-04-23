<template>
  <b-input-group class="p-4" v-on:keyup.enter='sendData()'>
    <template v-slot:prepend>
      <b-form-select :options="methods" size="sm" v-model="input.method" variant="info"></b-form-select>
    </template>
    <b-form-input placeholder='url' size="sm" type='text' v-model='input.url'></b-form-input>
    <b-input-group-append >
      <b-button size="sm" text="Button"  v-on:click='sendData()' variant="success">Send</b-button>
    </b-input-group-append>
  </b-input-group>
</template>
<script>
  import axios from 'axios'

  export default {
    name: 'url-caller',
    data () {
      return {
        methods: ['GET', 'POST'],
        input: {
          method: 'GET',
          url: ''
        },
        response: {}
      }
    },
    mounted () {},
    methods: {
      getResult (result) {
        this.response = result
      },
      sendData () {
        if (!this.input.url) return
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
        }).finally(() => this.$emit('call-url', this.response))
      }
    }
  }
</script>

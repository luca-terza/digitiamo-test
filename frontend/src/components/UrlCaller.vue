<template>
  <b-input-group class="p-4" v-on:keyup.enter='sendData()'>
    <template v-slot:prepend>
      <b-form-select :options="methods" size="sm" v-model="input.method" variant="info"></b-form-select>
    </template>
    <b-form-input placeholder='url' size="sm" type='text' v-model='input.url'></b-form-input>
    <b-input-group-append >
      <b-button size="sm"  v-on:click='sendData()' variant="secondary">Send</b-button>
    </b-input-group-append>
  </b-input-group>
</template>
<script>
  import axios from 'axios'

  export default {
    name: 'url-caller',
    data () {
      return {
        methods: [
          'GET',
          'POST',
          'PUT',
          'DELETE',
          'HEAD',
          'OPTIONS',
          'PATCH',
          'INFO',
          'DUMB'
        ],
        input: {
          method: 'GET',
          url: ''
        },
        response: {}
      }
    },
    mounted () {},
    methods: {
      sendData () {
        if (!this.input.url) return
        axios({
          method: 'POST',
          'url': 'http://localhost:5000/api/v1.0/request_url/' + this.input.method,
          'data': {'requested_url': this.input.url},
          'headers': {'content-type': 'application/json'}
        }).then(result => {
          this.response = result
          this.response['final_message'] = result.data.result.status_msg
        }).catch(error => {
          console.log(error)
          if (error.response) {
            this.response = error.response
            this.response['final_message'] = JSON.parse(error.response.data.result.errors).error
          } else if (error.hasOwnProperty('message')) {
            this.response['final_message'] = error.message
          }
        }).finally(() => this.$emit('call-url', this.response))
      }
    }
  }
</script>
<style lang="scss">
    .some-class {
      @media (max-width: 567px) {
        background-color: red;
      }

    }

</style>

<template>
  <b-input-group class="p-4">
    <template v-slot:prepend>
      <b-btn disabled> {{method}}</b-btn>
    </template>
    <b-col  class="btn btn-secondary disabled"> {{calledUrl}}</b-col>
  </b-input-group>
</template>
<script>
  export default {
    name: 'call-display',
    props: {
      'method': String,
      'calledUrl': String}
  }
</script>

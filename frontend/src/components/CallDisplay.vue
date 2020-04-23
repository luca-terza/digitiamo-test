<template>
  <b-input-group class="p-4">
    <template v-slot:prepend>
      <b-col class="btn btn-secondary disabled no-hand"> {{method}}</b-col>
    </template>
    <b-col class="btn btn-secondary disabled no-hand"> {{calledUrl}}</b-col>
  </b-input-group>
</template>
<script>
  export default {
    name: 'call-display',
    props: {
      'method': String,
      'calledUrl': String
    }
  }
</script>

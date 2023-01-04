<template>
  <div>
    <Header></Header>
    <div class="leftNav">
      <side-navigation></side-navigation>
      <router-view/>
    </div>
  </div>
</template>

<script>
import Header from "../common/Header";
import sideNavigation from "../common/sideNavigation";

export default {
  name: "index",
  components: {
    Header,
    sideNavigation
  }
}
</script>

<style scoped>
.leftNav {
  width: auto;
  min-height: 87vh;
}
</style>

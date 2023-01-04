<template>
  <div class="Header">
    <el-col :span="1.5"><el-avatar shape="square" :size="65" src="/static/logo.png"></el-avatar></el-col>
    <el-col :span="5"><h1>小区管理系统</h1></el-col>
    <div class="user">
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
      <p>{{ this.username }}</p>
      <el-button type="text" @click="signOut">退出系统</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      username: sessionStorage.getItem('user_name'),
    }
  },
  methods: {
    signOut() {
      localStorage.removeItem("user_token");
      localStorage.removeItem("user_name");
      localStorage.removeItem("user_id");
      localStorage.removeItem("stated");
      sessionStorage.removeItem("user_id");
      sessionStorage.removeItem("user_name");
      sessionStorage.removeItem("user_token");
      sessionStorage.removeItem("stated");
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.Header {
  width: 100%;
  min-height: 80px;
  background-color: rgb(2, 192, 206);
}
.Header h1 {
  position: absolute;
  /*text-indent: 1em;*/
}
.Header .el-avatar {
  margin: 5px 9px;
  border-radius: 12px;
}
.user {
  float: right;
  min-width: 7vw;
  line-height: 40px;
}
.user .el-avatar {
  float: right;
  margin: 10px;
  width: 50px;
  height: 50px;
}
.user .el-button {
  margin-top: 12px;
  float: right;
  color: black;
  display: inline-block;
  padding: 20px 20px;
}
.user .el-button:hover {
  color: white;
}
.user p {
  float: right;
}
</style>

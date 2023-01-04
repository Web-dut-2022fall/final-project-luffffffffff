<template>
  <div class="left-Nav">
    <el-col :span="6">
      <el-menu
          router
          background-color="#E0E0E0FF"
          text-color="#000000"
          active-text-color="#213A53FF">
<!--        物业-->
        <el-menu-item index="/admin/build" v-show="flag===2">
          <i class="el-icon-office-building"></i>
          <span slot="title">小区管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/house" v-show="flag===2">
          <i class="el-icon-s-home"></i>
          <span slot="title">住房管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/user" v-show="flag===2">
          <i class="el-icon-s-custom"></i>
          <span slot="title">住户管理</span>
        </el-menu-item>
<!--        住户-->
        <el-menu-item index="/household/home" v-show="flag===1">
          <i class="el-icon-s-home"></i>
          <span slot="title">首页</span>
        </el-menu-item>
        <el-menu-item index="/household/perInfo" v-show="flag===1">
          <i class="el-icon-user-solid"></i>
          <span slot="title">个人信息</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </div>
</template>

<script>
export default {
  name: "sideNavigation",
  data() {
    return {
      flag: parseInt(sessionStorage.getItem('stated')),
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.left-Nav {
  top: 0;
  position: sticky;
}
.left-Nav .el-col{
  height: 100vh;
  background-color: rgb(224, 224, 224);
}
</style>

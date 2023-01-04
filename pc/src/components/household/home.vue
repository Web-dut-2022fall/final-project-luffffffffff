<template>
  <el-col :span="18" class="Home">
    <el-row :gutter="40" class="headerCard">
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header" class="clearfix">
            <span class="el-icon-s-order">公告</span>
          </div>
          <div v-for="(o, index) in notices" :key="index" class="text item">
            {{ o.content }}
<!--            <span style="float: right">{{ o.message_date }}</span>-->
          </div>
          <el-button type="text" size="small" style="float: right" @click="dialogTableVisible = true">查看更多<i
            class="el-icon-d-arrow-right"></i></el-button>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header" class="clearfix">
            <span class="el-icon-message-solid">反馈信息</span>
          </div>
          <div v-for="(feedback, index) in feedbackData" :key="index" class="text item">
            {{ feedback.content }}
          </div>
          <el-button type="text" size="small" style="float: right" @click="dialogTable = true">查看更多<i class="el-icon-d-arrow-right"></i></el-button>
        </el-card>
      </el-col>
    </el-row>
    <div class="quickAccess">
      <div id="header">
        <el-col :span="1"><i class="el-icon-link"></i></el-col>
        <p>快速访问</p>
      </div>
      <div style="padding: 2vh" class="access">
        <el-col :span="4.8" v-for="(i, index) in access" :key="index">
          <router-link :to="i.rout">
            <el-card>
              <i :class="i.ava"></i>
            </el-card>
          </router-link>
        </el-col>
      </div>
    </div>
    <el-dialog title="公告列表" :visible.sync="dialogTableVisible">
      <el-table :data="gridData" height="400">
        <el-table-column property="message_date" label="日期" width="150"></el-table-column>
        <el-table-column property="content" label="公告内容"></el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="报修反馈" :visible.sync="dialogTable">
      <el-table :data="feedbackData" height="400">
        <el-table-column property="handle_date" label="处理日期" width="180"></el-table-column>
        <el-table-column property="content" label="报修内容"></el-table-column>
        <el-table-column property="stated" label="状态" width="70"></el-table-column>
      </el-table>
    </el-dialog>
  </el-col>
</template>

<script>
export default {
  name: "home",
  data() {
    return {
      access: [
        {rout: '/household/perInfo', ava: 'el-icon-user-solid'},
        {rout: '/household/home', ava: 'el-icon-menu'},
        {rout: '/household/home', ava: 'el-icon-warning'},
        {rout: '/household/home', ava: 'el-icon-coin'},
        {rout: '/household/home', ava: 'el-icon-chat-line-square'}
      ],
      notices: [{
        'content': '公告1'
      }, {
        'content': '公告2'
      }, {
        'content': '公告3'
      }],
      dialogTableVisible: false,
      dialogTable: false,
      gridData: [],
      moreFeed: [],
      feedbackData: [{
        'content': '反馈1'
      }, {
        'content': '反馈2'
      }, {
        'content': '反馈3'
      }]
    }
  },
  created() {
  },
  methods: {

  }
}
</script>

<style scoped>
.Home {
  padding: 20px;
  background-color: #f2f2f2;
  min-height: 100vh;
}

.Home .quickAccess {
  width: auto;
  height: 30vh;
  background-color: white;
  /*padding: 1vh;*/
}

.headerCard .el-card {
  height: 38vh;
}

.text {
  font-size: 2vh;
}

.item {
  margin-bottom: 3vh;

}

.quickAccess #header {
  width: auto;
  height: 6vh;
  border-bottom: #989494 solid 1px;
}

.quickAccess i {
  font-size: 2vw;
  padding: 1vh;
}

.quickAccess p {
  padding: 1.6vh 0;
}

.access {
  text-align: center;
}

.access .el-card {
  height: 19vh;
  background-color: #02C0CECC;
  margin-right: 4vw;
  cursor: pointer;
}

.access .el-card:hover {
  border: dimgrey solid 1px;
  background-color: #e9efef;
}

.access i {
  font-size: 13vh;
}
</style>

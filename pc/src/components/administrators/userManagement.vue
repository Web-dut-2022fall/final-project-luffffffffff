<template>
  <el-col :span="18" class="management">
    <el-card>
      <div v-show="addUser===0">
        <div class="userSearch">
          <el-input prefix-icon="el-icon-search" size="small" clearable placeholder="可输入姓名进行查询" v-model="searchWord"></el-input>
          <el-button type="primary" size="small" icon="el-icon-search" @click="search">搜索</el-button>
          <el-button type="success" icon="el-icon-plus" size="small" class="add" @click="addUser=1">增加住户</el-button>
        </div>
        <p>一共有{{ $store.state.users_length }}个住户</p>
        <div class="showInfo">
          <el-table
            :data="tableData"
            stripe
            style="width: 100%">
            <el-table-column
              fixed
              prop="username"
              label="用户名"
              width="150">
            </el-table-column>
            <el-table-column
              prop="first_name"
              label="姓名"
              width="120">
            </el-table-column>
            <el-table-column
              prop="rom_num"
              label="房号"
              width="100">
            </el-table-column>
            <el-table-column
              sortable
              prop="build_num"
              label="楼栋"
              width="100">
            </el-table-column>
            <el-table-column
              prop="car_num"
              label="车牌号"
              width="120">
            </el-table-column>
            <el-table-column
              label="激活状态"
              prop="is_active"
              width="100"
              :filters="[{ text: '未激活', value: 0 }, { text: '已激活', value: 1 }]"
              :filter-method="filterTag"
              filter-placement="bottom-end">
              <template slot-scope="scope">
                <el-result :icon="scope.row.is_active===1?'success':'error'"></el-result>
              </template>
            </el-table-column>
            <el-table-column
              prop="email"
              label="邮箱"
              width="255">
            </el-table-column>
            <el-table-column
              sortable
              prop="date_joined"
              label="加入时间"
              width="300">
            </el-table-column>
            <el-table-column
              fixed="right"
              label="操作"
              width="100">
              <template slot-scope="scope">
                <i @click="handleClick(scope.row)" class="el-icon-menu"></i>
                <i class="el-icon-delete-solid" @click="deleteUser(scope.row)"></i>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div class="page_info">
          <el-pagination
            background
            layout="prev, pager, next, sizes"
            :page-sizes="[3, 5, 9]"
            :page-size="filters.size"
            @size-change="sizeChange"
            @current-change="handleChange"
            :total="total">
          </el-pagination>
        </div>
      </div>
      <div v-show="addUser===1" class="addUser">
        <el-page-header @back="goBack" :content=content>
        </el-page-header>
        <div class="inputArea" v-if="flag===0">
          <div class="entry">
            <div class="Input">
              <label>用户名：</label>
              <el-input size="small" v-model="add.username"></el-input>
              <p>必填；长度为150个字符或以下；只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”。</p>
            </div>
            <div class="Input">
              <label>密码：</label>
              <el-input size="small" v-model="add.password"></el-input>
              <p>你的密码必须包含至少 8 个字符。<br>
                你的密码不能是一个常见密码。<br>
                你的密码不能全都是数字。</p>
            </div>
            <div class="Input">
              <label>密码确认：</label>
              <el-input size="small" v-model="add.passwordAgain" @blur="checkPwd"></el-input>
              <p>为了校验，请输入与上面相同的密码。</p>
            </div>
          </div>
          <div>
            <el-button type="primary" @click="submit">添加</el-button>
          </div>
        </div>
        <div class="userInfo" v-else>
          <div class="entry">
            <div class="Input">
              <label>用户名：</label>
              <el-input size="small" v-model="info.username"></el-input>
              <p>必填；长度为150个字符或以下；只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”。</p>
            </div>
            <div class="Input">
              <label>密码：</label>
              {{ '******' + '$' + info.password.split('$')[3] + '******' }}
              <p>密码原文未存储在系统中，因此无法看到该用户的密码。然而你可以通过<a href="">这个表单</a>来修改密码。</p>
            </div>
            <div class="subHeader">个人信息</div>
            <div class="Input">
              <label>名字：</label>
              <el-input size="small" v-model="info.lastName"></el-input>
            </div>
            <div class="Input">
              <label>姓氏：</label>
              <el-input size="small" v-model="info.firstName"></el-input>
            </div>
            <div class="Input">
              <label>电子邮件：</label>
              <el-input size="small" v-model="info.email"></el-input>
            </div>
            <div class="Input">
              <label>性别：</label>
              <el-radio v-model="info.sex" label="0" border size="medium">男</el-radio>
              <el-radio v-model="info.sex" label="1" border size="medium">女</el-radio>
            </div>
            <div class="Input">
              <label>手机号：</label>
              <el-input size="small" v-model="info.mobile"></el-input>
            </div>
            <div class="subHeader">住房信息</div>
            <div class="Input">
              <label>房号：</label>
              <el-input size="small" v-model="info.rom_num"></el-input>
            </div>
            <div class="Input">
              <label>车牌号：</label>
              <el-input size="small" v-model="info.car_num"></el-input>
            </div>
            <div class="Input">
              <label>所在楼栋：</label>
              <el-input size="small" v-model="info.build_num"></el-input>
            </div>
            <div class="Input">
              <label>住房所在单元：</label>
              <el-input size="small" v-model="info.uni_num"></el-input>
            </div>
            <div class="subHeader">权限</div>
            <el-col :span="18">
              <el-checkbox v-model="checked.activate">激活状态</el-checkbox>
              <p>指明用户是否被认为是活跃的。以反选代替删除帐号。</p>
            </el-col>
            <el-col :span="18">
              <el-checkbox v-model="checked.worker">工作人员状态</el-checkbox>
              <p>指明用户是否可以登录到这个管理站点</p>
            </el-col>
            <el-col :span="18">
              <el-checkbox v-model="checked.superuser">超级用户状态</el-checkbox>
              <p>指明该用户缺省拥有所有权限。</p>
            </el-col>
          </div>
          <div class="submit-bottom">
            <el-button class="el-icon-arrow-left" size="small" @click="goBack">返回</el-button>
            <el-button class="el-icon-delete" size="small" type="danger">删除</el-button>
            <el-button size="small" type="primary" @click="userSave">保存</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </el-col>
</template>

<script>
import moment from "moment";

export default {
  name: "userManagement",
  inject: ['reload'],
  data() {
    return {
      sign: '1',
      checked: {
        activate: '',
        worker: '',
        superuser: '',
      },
      content: "添加住户",
      flag: 0,
      filters: {
        size: 9,   //单页显示条数
        page: 1,   //当前页码
      },
      add: {
        username: '',
        password: '',
        passwordAgain: '',
      },
      info: {
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        email: '',
        sex: '',
        mobile: '',
        rom_num: '',
        car_num: '',
        uni_num: '',
        build_num: ''
      },
      total: 0,
      searchWord: '',
      tableData: [],
      addUser: 0,
    }
  },
  created() {
    this.getUser();
  },
  methods: {
    filterTag(value, row) {
      return row.is_active === value;
    },
    getUser() {
      let filters = {
        page: this.filters.page,
        size: this.filters.size,
      };
      this.$axios.get(`${this.$settings.HOST}/user/management/`, {
        params: filters
      }).then(response => {
        this.tableData = response.data.results;
        this.$store.commit("del_user", response.data.count);
        this.total = response.data.count;
        let tableData = this.tableData;
        for (const data in tableData) {
          this.tableData[data]['first_name'] = tableData[data]['first_name'] + tableData[data]['last_name'];
          this.tableData[data]['date_joined'] = moment(this.tableData[data]['date_joined']).format('YYYY-MM-DD HH:mm:ss')
          if (this.tableData[data]['email'] === '') {
            this.tableData[data]['email'] = '未填写'
          } else if (this.tableData[data]['first_name'] === '') {
            this.tableData[data]['first_name'] = '未填写'
          }
          if (this.tableData[data]['is_active'] === true) {
            this.tableData[data]['is_active'] = 1
          } else {
            this.tableData[data]['is_active'] = 0
          }
        }
      }).catch(error => {
        console.log(error.response);
      });
    },
    deleteUser(row) {
      this.$axios.delete(`${this.$settings.HOST}/user/info/`, {
        params: {
          uid: row.id,
        },
      }).then(response => {
        this.$message.success(response.data.msg);
        this.$store.commit("del_user", response.data.length);
        this.reload();
      }).catch(error => {
        this.$message.error(error.response);
      });
    },
    goBack() {
      this.addUser = 0;
      this.reload();
    },
    handleClick(row) {
      sessionStorage.uuid = row.id;
      this.flag = this.addUser = 1;
      this.content = '修改住户';
      this.$axios.patch(`${this.$settings.HOST}/user/info/`, {
        uid: row.id,
      }).then(response => {
        this.info.username = response.data.username;
        this.info.password = response.data.password;
        this.info.firstName = response.data.first_name;
        this.info.lastName = response.data.last_name;
        this.info.email = response.data.email;
        this.info.mobile = response.data.mobile;
        this.info.rom_num = response.data.rom_num;
        this.info.car_num = response.data.car_num;
        this.info.build_num = response.data.build_num;
        this.info.uni_num = response.data.uni_num;
        this.info.sex = response.data.sex === '男' ? '0' : '1'
        this.checked.superuser = response.data.is_superuser;
        this.checked.activate = response.data.is_active;
        this.checked.worker = response.data.stated === "0";
      }).catch(error => {
        console.log(error.response.data);
      });
    },
    userSave() {
      this.$axios.put(`${this.$settings.HOST}/user/info/`, {
        username: this.info.username,
        email: this.info.email,
        first_name: this.info.firstName,
        last_name: this.info.lastName,
        is_active: this.checked.activate,
        is_superuser: this.checked.superuser,
        stated: this.checked.worker,
        sex: this.info.sex,
        mobile: this.info.mobile,
        rom_num: this.info.rom_num,
        car_num: this.info.car_num,
        build_num: this.info.build_num,
        uni_num: this.info.uni_num,
        uid: sessionStorage.getItem('uuid'),
      }).then(response => {
        this.$message.success(response.data.msg);
        this.reload();
      }).catch(error => {
        console.log(error.response);
      });
    },
    handleChange(page) {
      console.log("本次点击的页码:", page);
      this.filters.page = page;
      this.getUser();
    },
    sizeChange(size) {
      this.filters.size = size;
      this.filters.page = 1;
      this.getUser();
    },
    checkPwd() {
      if (this.add.password !== this.add.passwordAgain) {
        this.$message.error('两次输入密码不一致！');
        return false;
      }
    },
    search() {
      // this.$message.success(this.searchWord);
      this.$axios.post(`${this.$settings.HOST}/user/search/`, {
        key: this.searchWord,
      }).then(response => {
        this.tableData = response.data;
        this.$store.commit("del_user", response.data.count);
        let tableData = this.tableData;
        for (const data in tableData) {
          this.tableData[data]['first_name'] = tableData[data]['first_name'] + tableData[data]['last_name'];
          this.tableData[data]['date_joined'] = moment(this.tableData[data]['date_joined']).format('YYYY-MM-DD HH:mm:ss')
          if (this.tableData[data]['email'] === '') {
            this.tableData[data]['email'] = '未填写'
          } else if (this.tableData[data]['first_name'] === '') {
            this.tableData[data]['first_name'] = '未填写'
          }
          if (this.tableData[data]['is_active'] === true) {
            this.tableData[data]['is_active'] = 1
          } else {
            this.tableData[data]['is_active'] = 0
          }
        }
        this.$message.success('查找成功');
      }).catch(error => {
        this.$message.error('查找失败');
      });
    },
    submit() {
      if (this.checkPwd() === false) {
        return false;
      }
      this.$axios.post(`${this.$settings.HOST}/user/`, {
        username: this.add.username,
        password: this.add.passwordAgain,
        stated: this.sign,
        is_active: this.sign,
      }).then(response => {
        console.log(response.data);
        this.$message.success('添加用户成功！');
        this.$notify({
          title: '警告',
          message: '请立刻前去完善信息',
          type: 'warning',
          duration: 6000
        });
        this.add.username = '';
        this.add.password = '';
        this.add.passwordAgain = '';
      }).catch(error => {
        this.$message.error(error);
      });
    }
  }
}
</script>

<style scoped>
.management {
  min-height: 100vh;
  padding: 20px;
  background-color: rgb(241, 241, 241);
}

.management .el-card {
  min-height: 95vh;
  /*padding: 20px;*/
}

.management >>> .el-card__body {
  padding: 0;
}

.userSearch {
  width: auto;
  height: 35px;
  padding: 8px;
  background-color: rgb(248, 248, 248);
  border-bottom: #dcdcdc solid 1px;
}

.userSearch .el-input {
  width: 240px;
  margin-right: 2vw;
}

.userSearch .add {
  float: right;
}

.showInfo {
  padding: 20px;
}

.showInfo >>> .el-table thead {
  color: rgb(2, 192, 208);
}

.showInfo .el-result {
  padding: 0;
}

.showInfo >>> .el-result__icon svg {
  width: 20px;
  height: 20px;
}

.showInfo i {
  padding-right: 20px;
  cursor: pointer;
}

.showInfo i:hover:nth-child(1) {
  color: rgb(64, 158, 255);
}

.showInfo i:hover:nth-child(2) {
  color: rgb(255, 64, 80);
}

.el-card p {
  font-size: 10px;
  color: silver;
  padding-left: 10px;
}

.el-card .page_info {
  text-align: center;
  position: absolute;
  left: 55%;
  bottom: -50px;
}

.addUser {
  padding: 20px;
}

.addUser .el-page-header {
  padding: 10px;
}

.inputArea .el-button {
  float: right;
  margin-right: 20px;
}

.entry {
  padding: 20px;
  margin-bottom: 30px;
  min-height: 50vh;
}

.entry .subHeader {
  width: auto;
  height: 3vh;
  background-color: #333;
  color: white;
  padding: 5px;
  margin-bottom: 15px;
}

.entry .Input {
  padding-bottom: 30px;
}

.entry .el-col {
  padding-bottom: 10px;
}

.Input .el-input {
  width: 250px;
}

.Input label {
  display: inline-block;
  width: 230px;
  font-weight: bolder;
}

.Input p {
  padding-left: 235px;
  color: dimgrey;
}

.submit-bottom {
  margin-top: 170px;
  width: auto;
  height: 7vh;
  padding: 10px;
}
</style>

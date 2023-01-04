<template>
  <div class="login">
    <div v-show="this.flag" class="houseForm">
      <el-form :inline="true" :model="form" label-width="80px">
        <el-form-item label="姓氏" prop="firstName">
          <el-input v-model="form.first_name"></el-input>
        </el-form-item>
        <el-form-item label="名字" prop="lastName">
          <el-input v-model="form.last_name"></el-input>
        </el-form-item>
        <el-form-item label="住房楼栋" prop="romNum">
          <el-input v-model="form.build_num" placeholder="如：13栋"></el-input>
        </el-form-item>
        <el-form-item label="房号" prop="houseNum">
          <el-input v-model="form.rom_num" placeholder="如：1301"></el-input>
        </el-form-item>
        <el-form-item label="住房单元">
          <el-input v-model="form.uni_num" placeholder="如：一单元"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="sex">
          <el-radio-group v-model="form.sex" size="medium">
            <el-radio border label="男"></el-radio>
            <el-radio border label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <el-form :model="form" label-width="70px">
        <el-form-item label="邮箱">
          <el-col :span="14">
            <el-input v-model="form.email"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="车牌号">
          <el-col :span="4">
            <el-input v-model="form.carnum1" placeholder="如：桂A"></el-input>
          </el-col>
          <el-col style="text-align: center" :span="2">--</el-col>
          <el-col :span="12">
            <el-input v-model="form.carnum2" placeholder="如：597Y8"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="手机号" prop="mobile">
          <el-col :span="14">
            <el-input v-model="form.mobile"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="HouseSave">提交</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-if="token" class="already">
      <h1>
        您已登录，请前往
        <router-link to="/home">主页</router-link>
      </h1>
    </div>
    <div class="loginBox" v-else>
      <div class="title">
        <span @click="Type=0">登录</span>
        <span @click="Type=1">注册</span>
      </div>
      <div v-show="Type===0" class="Box">
        <div class="Input">
          <el-input v-model="login.username" placeholder="请输入账号" clearable></el-input>
          <el-input v-model="login.password" placeholder="请输入密码" show-password></el-input>
        </div>
        <div class="btn">
          <el-button type="primary" @click="Login">登录</el-button>
        </div>
      </div>
      <div v-show="Type===1" class="Box">
        <div class="Input">
          <el-input v-model="reg.username" placeholder="请输入注册用户名" clearable></el-input>
          <el-input v-model="reg.password" placeholder="请输入密码" show-password></el-input>
        </div>
        <div class="switch">
          <el-radio v-model="chose" label="1">住户</el-radio>
          <el-radio v-model="chose" label="2">物业人员</el-radio>
        </div>
        <div class="btn">
          <el-button type="success" @click="Register">注册</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "index",
  inject: ['reload'],
  data() {
    return {
      flag: false,
      chose: '',
      active: '1',
      token: '',
      bridge: '',
      Type: 0,
      form: {
        first_name: '',
        last_name: '',
        build_num: '',
        rom_num: '',
        uni_num: '',
        sex: '',
        email: '',
        carnum1: '',
        carnum2: '',
        mobile: '',
      },
      login: {
        username: '',
        password: '',
      },
      reg: {
        username: '',
        password: '',
      },
    }
  },
  created() {
    this.check_user_login();
  },
  methods: {
    check_user_login() {
      this.token = sessionStorage.user_token || localStorage.user_token;
      return this.token;
    },
    Login() {
      if (this.login.password === '' || this.login.username === '') {
        this.$message.error('账号或密码不能为空');
        return false;
      }
      this.$axios.post(`${this.$settings.HOST}/user/login/`, {
        username: this.login.username,
        password: this.login.password,
      }).then(response => {
        localStorage.removeItem("user_token");
        localStorage.removeItem("user_name");
        localStorage.removeItem("user_id");
        localStorage.removeItem("stated");
        sessionStorage.user_token = response.data.token;
        sessionStorage.user_id = response.data.id;
        sessionStorage.user_name = response.data.name;
        sessionStorage.stated = response.data.stated;
        let self = this;
        this.$alert('登录成功', '小区管理系统', {
          callback() {
            self.$router.push('/home');
          }
        });
      }).catch(error => {
        this.$message.error('账号密码错误');
      });
    },
    Register() {
      if (this.chose === '') {
        this.$message.error('请选择注册类型!');
        console.log(this.chose);
        return false;
      } else if (this.chose === '2') {
        this.$axios.post(`${this.$settings.HOST}/user/`, {
          username: this.reg.username,
          password: this.reg.password,
          stated: this.chose,
          is_active: this.active,
        }).then(response => {
          sessionStorage.user_token = response.data.token;
          sessionStorage.user_id = response.data.id;
          sessionStorage.user_name = response.data.username;
          sessionStorage.stated = response.data.stated;
          this.$alert('注册成功！', '小区管理系统', {
            callback() {
              self.$router.push('/home');
            }
          });
        }).catch(error => {
          let data = error.response.data;
          let message = "";
          for (let key in data) {
            message = data[key][0];
          }
          this.$message.error(message);
        });
      } else {
        this.$axios.post(`${this.$settings.HOST}/user/`, {
          username: this.reg.username,
          password: this.reg.password,
          stated: this.chose,
          is_active: this.active,
        }).then(response => {
          console.log(response.data);
          localStorage.removeItem("user_id");
          localStorage.removeItem("user_name");
          localStorage.removeItem("stated");
          this.bridge = response.data.token;
          sessionStorage.user_id = response.data.id;
          sessionStorage.user_name = response.data.username;
          sessionStorage.stated = response.data.stated;
        }).catch(error => {
          this.$message.error(error.response.data);
          console.log(error.response.data);
        });
        this.flag = true;
        this.$alert('注册成功，完善资料后，方可进入系统！', '小区管理系统');
      }
    },
    HouseSave() {
      this.$axios.post(`${this.$settings.HOST}/user/info/`, {
        info: this.form,
        uid: sessionStorage.getItem('user_id'),
      }).then(response => {
        localStorage.removeItem("user_token");
        sessionStorage.user_token = this.bridge;
        let self = this;
        this.$alert('提交成功', '小区管理系统', {
          callback() {
            self.$router.push('/home');
          }
        });
      }).catch(error => {
        let data = error.response.data;
        let message = "";
        for (let key in data) {
          message = data[key][0];
        }
        this.$message.error(message);
      });
    }
  }
}
</script>

<style scoped>
.login {
  background: url("../../static/login/background.jpg");
  width: 100%;
  height: 100%;
  position: fixed;
  background-size: 100% 100%;
}

.login .houseForm {
  position: absolute;
  background-color: white;
  height: 400px;
  width: 600px;
  margin: 5% 33%;
  border-radius: 8px;
  z-index: 9;
  padding: 40px 30px;
}

.loginBox {
  margin: 8% 38%;
  width: 24%;
  min-height: 30vh;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(20px) saturate(200%);
}

.loginBox a {
  padding-top: 20px;
  padding-right: 15px;
  float: right;
  text-decoration: none;
  color: rgb(6, 6, 162);
}

.loginBox a:hover {
  color: white;
}

.loginBox .title {
  text-align: center;
  padding: 10px;
  border-bottom: 1px solid darkblue;
}

.loginBox .title span {
  font-size: 20px;
  color: rgba(37, 37, 115, 0.51);
  cursor: pointer;
  padding: 0 20px;
}

.loginBox .title span:hover {
  color: white;
}

.Box {
  padding: 20px;
}

.Box .btn {
  text-align: center;
}

.Box .el-button {
  border-radius: 8px;
  padding: 12px 126px;
}

.Box .Input {
  padding: 15px 20px;
}

.Box .Input .el-input {
  padding: 20px 0;
}

.Box .switch {
  text-align: center;
  padding-bottom: 10px;
}

.already h1 {
  padding: 10vh 15vw;
  font-size: 100px;
}
</style>

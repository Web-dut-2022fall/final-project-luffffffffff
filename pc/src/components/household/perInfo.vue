<template>
  <div class="perInfo">
    <el-col :span="18">
      <div class="cardUser">
        <div class="avatar">
          <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
        </div>
      </div>
      <div class="boxUser">
        <div class="Header">
          <h1>基本信息</h1>
        </div>
        <div class="Info">
          <ul>
            <li>
              <span>用户昵称</span>
              {{ infoList.username }}
              <div class="edit">
                <el-button type="text" @click="editClick=1, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
            <li>
              <span>用&nbsp;户&nbsp;&nbsp;ID</span>
              user_{{ infoList.id }}
              <div class="edit">
                <el-button type="text" disabled>不可编辑</el-button>
              </div>
            </li>
            <li>
              <span>姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名</span>
              {{ allName }}
              <div class="edit">
                <el-button type="text" @click="editClick=2, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
            <li>
              <span>用户邮箱</span>
              {{ infoList.email }}
              <div class="edit">
                <el-button type="text" @click="editClick=3, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
            <li>
              <span>手机号码</span>
              {{ infoList.mobile }}
              <div class="edit">
                <el-button type="text" @click="editClick=4, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
            <li>
              <span>性别</span>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              {{ infoList.sex }}
              <div class="edit">
                <el-button type="text" @click="editClick=5, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
          </ul>
        </div>
        <el-dialog title="修改信息" :visible.sync="dialogFormVisible" :before-close="handleClose">
          <el-form :model="form" :label-width="formLabelWidth">
            <el-form-item label="用户昵称" v-show="editClick===1">
              <el-input v-model="form.name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="姓氏" v-show="editClick===2">
              <el-input v-model="form.firstName" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="名字" v-show="editClick===2">
              <el-input v-model="form.lastName" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" v-show="editClick===3">
              <el-input v-model="form.email" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" v-show="editClick===4">
              <el-input v-model="form.mobile" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="性别" v-show="editClick===5">
              <el-radio-group v-model="form.sex" size="medium">
                <el-radio border label="男"></el-radio>
                <el-radio border label="女"></el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="房号" v-show="editClick===6">
              <el-input v-model="form.rom_num" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="楼栋数" v-show="editClick===7">
              <el-input v-model="form.build_num" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="单元数" v-show="editClick===8">
              <el-input v-model="form.uni_num" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="车牌号" v-show="editClick===9">
              <el-col :span="4">
                <el-input v-model="form.carnum1" autocomplete="off"></el-input>
              </el-col>
              <el-col style="text-align: center" :span="2">--</el-col>
              <el-col :span="12">
                <el-input v-model="form.carnum2" autocomplete="off"></el-input>
              </el-col>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="dialogFormVisible = false, save()">保 存</el-button>
          </div>
        </el-dialog>
      </div>
      <div class="boxUser">
        <div class="Header">
          <h1>住房信息</h1>
        </div>
        <div class="Info">
          <ul>
            <li>
              <span>房&nbsp&nbsp&nbsp号</span>
              {{ infoList.rom_num }}
              <div class="edit">
                <el-button type="text" @click="editClick=6, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
            <li>
              <span>楼栋数</span>
              {{ infoList.build_num }}
              <div class="edit">
                <el-button type="text" @click="editClick=7, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
            <li>
              <span>单元数</span>
              {{ infoList.uni_num }}
              <div class="edit">
                <el-button type="text" @click="editClick=8, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
            <li>
              <span>车牌号</span>
              {{ infoList.car_num }}
              <div class="edit">
                <el-button type="text" @click="editClick=9, dialogFormVisible = true">编辑</el-button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </el-col>
  </div>
</template>

<script>
export default {
  name: "perInfo",
  inject: ['reload'],
  data() {
    return {
      uid: sessionStorage.getItem('user_id'),
      editClick: 0,
      dialogFormVisible: false,
      Data: '',
      allName: '',
      form: {
        name: '',
        firstName: '',
        lastName: '',
        email: '',
        sex: '',
        rom_num: '',
        build_num: '',
        uni_num: '',
        carnum1: '',
        carnum2: '',
      },
      infoList: [],
      formLabelWidth: '120px',
    }
  },
  mounted: function () {
    this.$axios.patch(`${this.$settings.HOST}/user/info/`, {
      uid: this.uid,
    }).then(res => {
      this.infoList = res.data;
      this.allName = res.data.first_name + res.data.last_name;
    }).catch(error => {
      this.$message.error(error.response.data);
    });
  },
  methods: {
    handleClose(done) {
      this.$confirm('确定取消修改？')
        .then(_ => {
          done();
        })
        .catch(_ => {
        });
    },
    save() {
      console.log(this.editClick);
      if (this.editClick === 1) {
        this.Data = this.form.name;
      }
      if (this.editClick === 2) {
        this.Data = this.form.firstName + ',' + this.form.lastName;
      }
      if (this.editClick === 3) {
        this.Data = this.form.email;
      }
      if (this.editClick === 4) {
        this.Data = this.form.mobile;
      }
      if (this.editClick === 5) {
        this.Data = this.form.sex;
      }
      if (this.editClick === 6) {
        this.Data = this.form.rom_num;
      }
      if (this.editClick === 7) {
        this.Data = this.form.build_num;
      }
      if (this.editClick === 8) {
        this.Data = this.form.uni_num;
      }
      if (this.editClick === 9) {
        this.Data = this.form.carnum1 + this.form.carnum2;
      }
      this.$axios.post(`${this.$settings.HOST}/user/info/`, {
        flag: this.editClick,
        uid: this.uid,
        info: this.Data,
      }).then(res => {
        console.log(res.data.msg);
        this.$message({
          message: '信息保存成功',
          type: 'success'
        });
        this.reload();
      }).catch(error => {
        console.log(error.response.data);
      });
    }
  }
}
</script>

<style scoped>
.perInfo {
  height: 120vh;
}

.perInfo .Header {
  width: auto;
  height: 50px;
  border-bottom: 1px solid #c0c0c0;
}

.perInfo .cardUser {
  width: auto;
  height: 140px;
}

.cardUser .avatar {
  width: 30vw;
  height: 130px;
  /*text-align: center;*/
  padding-top: 10px;
  padding-left: 25px;
}

.cardUser .el-avatar {
  width: 90px;
  height: 90px;
}

.boxUser {
  box-shadow: 3px 3px 7px dimgrey;
}

.perInfo .Info {
  width: auto;
  min-height: 300px;
}

.Header h1 {
  font-size: 25px;
  margin-block-start: 0;
  margin-block-end: 0;
  padding: 8px;
}

.Info ul {
  list-style-type: none;
}

.Info li {
  padding-bottom: 32px;
  width: 30vw;
}

.Info .edit {
  position: absolute;
  margin: -31px 25vw;
  cursor: pointer;
  opacity: 0;
}

.Info li:hover .edit {
  opacity: 1;
}

.Info span {
  margin-right: 30px;
}
</style>

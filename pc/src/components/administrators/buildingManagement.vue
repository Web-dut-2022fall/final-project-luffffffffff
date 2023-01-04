<template>
  <el-col :span="18" class="buildManage">
    <el-card class="build_manage">
      <div v-show="addBuild===0">
        <div class="buildSearch">
          <el-input prefix-icon="el-icon-search" size="small" placeholder="可输入楼栋名进行查询" v-model="searchWord"></el-input>
          <el-button type="primary" size="small" icon="el-icon-search" @click="search">搜索</el-button>
          <el-button type="success" icon="el-icon-plus" size="small" class="add" @click="addBuild=1">增加楼栋</el-button>
        </div>
        <p>一共有{{ $store.state.build_length }}栋楼</p>
        <div class="page_info" v-show="total>=5">
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
        <el-col :span="12" :offset="6" class="showBuild">
          <el-table
            :data="tableData"
            stripe
            style="width: 500px">
            <el-table-column
              prop="name"
              label="楼栋名称"
              width="150">
            </el-table-column>
            <el-table-column
              sortable
              prop="house_num"
              label="楼栋住房数"
              width="120">
            </el-table-column>
            <el-table-column
              label="开盘状态"
              prop="stated"
              width="100"
              :filters="[{ text: '未开盘', value: 0 }, { text: '已开盘', value: 1 }]"
              :filter-method="filterTag"
              filter-placement="bottom-end">
              <template slot-scope="scope">
                <el-result :icon="scope.row.stated===1?'success':'error'"></el-result>
              </template>
            </el-table-column>
            <el-table-column
              fixed="right"
              label="操作"
              width="100">
              <template slot-scope="scope">
                <i @click="handleClick(scope.row)" class="el-icon-menu"></i>
                <i class="el-icon-delete-solid" @click="deleteBuild(scope.row)"></i>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </div>
      <div v-show="addBuild===1" class="addBuild">
        <el-page-header @back="goBack" :content=content>
        </el-page-header>
        <div class="inputBuild" v-if="flag===0">
          <div class="buildEntry">
            <div class="buildInput">
              <label>楼栋名称：</label>
              <el-input size="small" v-model="add.name"></el-input>
            </div>
            <div class="buildInput">
              <label>楼栋住房数：</label>
              <el-input size="small" v-model="add.house_num"></el-input>
            </div>
            <div class="buildInput">
              <label>开盘状态：</label>
              <el-radio v-model="add.stated" label="0" border size="medium">未开盘</el-radio>
              <el-radio v-model="add.stated" label="1" border size="medium">已开盘</el-radio>
            </div>
          </div>
          <div>
            <el-button type="primary" @click="submit">添加</el-button>
          </div>
        </div>
        <div class="inputBuild" v-else>
          <div class="buildEntry">
            <div class="buildInput">
              <label>楼栋名称：</label>
              <el-input size="small" v-model="info.name"></el-input>
            </div>
            <div class="buildInput">
              <label>楼栋住房数：</label>
              <el-input size="small" v-model="info.house_num"></el-input>
            </div>
            <div class="buildInput">
              <label>开盘状态：</label>
              <el-checkbox v-model="info.stated">开盘</el-checkbox>
            </div>
          </div>
          <div class="submit--bottom">
            <el-button class="el-icon-arrow-left" size="small" @click="goBack">返回</el-button>
            <el-button class="el-icon-delete" size="small" type="danger">删除</el-button>
            <el-button size="small" type="primary" @click="buildSave">保存</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </el-col>

</template>

<script>
export default {
  inject: ['reload'],
  name: "buildingManagement",
  data() {
    return {
      searchWord: '',
      addBuild: 0,
      content: "添加楼栋",
      flag: 0,
      total: 0,
      filters: {
        size: 5,   //单页显示条数
        page: 1,   //当前页码
      },
      add: {
        name: '',
        house_num: '',
        stated: '',
      },
      info: {
        name: '',
        house_num: '',
        stated: '',
      },
      tableData: [],
    }
  },
  created() {
    this.getBuild();
  },
  methods: {
    filterTag(value, row) {
      return row.stated === value;
    },
    getBuild() {
      let filters = {
        page: this.filters.page,
        size: this.filters.size,
      };
      this.$axios.get(`${this.$settings.HOST}/build/management/`, {
        params: filters
      }).then(response => {
        this.tableData = response.data.results;
        this.$store.commit("del_build", response.data.count);
        this.total = response.data.count;
      }).catch(error => {
        console.log(error.response);
      });
    },
    goBack() {
      this.addBuild = 0;
      this.reload();
    },
    deleteBuild(row) {
      this.$axios.delete(`${this.$settings.HOST}/build/`, {
        params: {
          bid: row.id,
        },
      }).then(response => {
        this.$message.success(response.data.msg);
        this.$store.commit("del_build", response.data.length);
        this.reload();
      }).catch(error => {
        this.$message.error(error.response);
      });
    },
    handleClick(row) {
      sessionStorage.bbid = row.id;
      this.flag = this.addBuild = 1;
      this.content = '修改楼栋信息';
      this.$axios.patch(`${this.$settings.HOST}/build/`, {
        bid: row.id,
      }).then(response => {
        this.info.name = response.data.name;
        this.info.house_num = response.data.house_num;
        this.info.stated = response.data.stated === 1;
      }).catch(error => {
        console.log(error.response.data);
      });
    },
    buildSave() {
      this.$axios.put(`${this.$settings.HOST}/build/`, {
        data: this.info,
        bid: sessionStorage.getItem('bbid'),
      }).then(response => {
        this.$message.success(response.data.msg);
        this.reload();
      }).catch(error => {
        console.log(error.response);
      });
    },
    submit() {
      this.$axios.post(`${this.$settings.HOST}/build/`, {
        info: this.add,
      }).then(response => {
        console.log(response.data);
        this.$message.success('添加楼栋成功！');
        this.add.name = '';
        this.add.house_num = '';
        this.add.stated = '';
      }).catch(error => {
        this.$message.error(error);
      });
    },
    search() {
      this.$axios.post(`${this.$settings.HOST}/build/search/`, {
        key: this.searchWord,
      }).then(response => {
        console.log(response.data);
        this.tableData = response.data;
        this.$store.commit("del_build", response.data.length);
        this.$message.success('查找成功');
      }).catch(error => {
        this.$message.error('查找失败');
      });
    },
    handleChange(page) {
      console.log("本次点击的页码:", page);
      this.filters.page = page;
      this.getBuild();
    },
    sizeChange(size) {
      this.filters.size = size;
      this.filters.page = 1;
      this.getBuild();
    },
  }
}
</script>

<style scoped>
.buildManage {
  min-height: 100vh;
  padding: 20px;
  background-color: rgb(241, 241, 241);
}

.buildManage .build_manage {
  min-height: 95vh;
}

.buildManage .build_manage >>> .el-card__body {
  padding: 0;
}

.showHeader h1 {
  margin-block-start: 0;
}

.buildSearch {
  width: auto;
  height: 35px;
  padding: 8px;
  background-color: rgb(248, 248, 248);
  border-bottom: #dcdcdc solid 1px;
}

.buildSearch .el-input {
  width: 240px;
  padding-right: 20px;
}

.buildSearch .add {
  float: right;
}

.showBuild {
  padding: 20px;
}
.showBuild >>> .el-table thead {
  color: rgb(2, 192, 208);
}

.showBuild .el-result {
  padding: 0;
}

.showBuild >>> .el-result__icon svg {
  width: 20px;
  height: 20px;
}

.showBuild i {
  padding-right: 20px;
  cursor: pointer;
}

.showBuild i:hover:nth-child(1) {
  color: rgb(64, 158, 255);
}

.showBuild i:hover:nth-child(2) {
  color: rgb(255, 64, 80);
}

.build_manage p {
  font-size: 10px;
  color: silver;
  padding-left: 10px;
}

.addBuild {
  padding: 20px;
}

.addBuild .el-page-header {
  padding: 10px;
}

.inputBuild .el-button {
  float: right;
  margin-right: 20px;
}

.buildEntry {
  padding: 20px;
  margin-bottom: 30px;
  min-height: 30vh;
}

.buildEntry .subHeader {
  width: auto;
  height: 3vh;
  background-color: #333;
  color: white;
  padding: 5px;
  margin-bottom: 15px;
}

.buildEntry .buildInput {
  padding-bottom: 30px;
}

.buildEntry .el-col {
  padding-bottom: 10px;
}

.buildInput .el-input {
  width: 250px;
}

.buildInput label {
  display: inline-block;
  width: 230px;
  font-weight: bolder;
}

.buildInput p {
  padding-left: 235px;
  color: dimgrey;
}

.submit--bottom {
  margin-top: 10vh;
  width: auto;
  height: 7vh;
  padding: 10px;
}

.el-card .page_info {
  text-align: center;
}
</style>

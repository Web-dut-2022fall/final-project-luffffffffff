<template>
  <el-col :span="18" class="houseManage">
    <el-card class="house_manage">
      <div v-show="addHouse===0">
        <div class="houseSearch">
          <el-input prefix-icon="el-icon-search" v-model="searchWord" size="small" placeholder="可输入用户id进行查询"></el-input>
          <el-button type="primary" size="small" icon="el-icon-search" @click="search">搜索</el-button>
          <el-button type="success" icon="el-icon-plus" size="small" class="add" @click="addHouse=1, getBuildId()">
            增加住房
          </el-button>
        </div>
        <p>一共有{{ $store.state.house_length }}个住房</p>
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
        <div class="showHouse">
          <el-table
            :data="tableData"
            stripe
            style="width: 830px">
            <el-table-column
              prop="house_id"
              label="房号"
              width="150">
            </el-table-column>
            <el-table-column
              prop="house_type"
              label="户型"
              width="120">
            </el-table-column>
            <el-table-column
              label="售出状态"
              prop="stated"
              width="100"
              :filters="[{ text: '未售出', value: 0 }, { text: '已售出', value: 1 }]"
              :filter-method="filterTag"
              filter-placement="bottom-end">
              <template slot-scope="scope">
                <el-result :icon="scope.row.stated===1?'success':'error'"></el-result>
              </template>
            </el-table-column>
            <el-table-column
              prop="uni"
              label="所属单元"
              width="120">
            </el-table-column>
            <el-table-column
              sortable
              prop="area"
              label="面积（m²）"
              width="120">
            </el-table-column>
            <el-table-column
              prop="building"
              label="所属楼栋"
              width="120">
            </el-table-column>
            <el-table-column
              fixed="right"
              label="操作"
              width="100">
              <template slot-scope="scope">
                <i @click="handleClick(scope.row)" class="el-icon-menu"></i>
                <i class="el-icon-delete-solid" @click="deleteHouse(scope.row)"></i>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <div v-show="addHouse===1" class="addHouse">
        <el-page-header @back="goBack" :content=content>
        </el-page-header>
        <div class="inputHouse" v-if="flag===0">
          <div class="houseEntry">
            <div class="houseInput">
              <label>房号：</label>
              <el-input size="small" v-model="add.house_id"></el-input>
            </div>
            <div class="houseInput">
              <label>占地面积(m²)：</label>
              <el-input size="small" v-model="add.area"></el-input>
            </div>
            <div class="houseInput">
              <label>户主id：</label>
              <el-input size="small" v-model="add.household"></el-input>
            </div>
            <div class="houseInput">
              <label>售价(元/m²)</label>
              <el-input size="small" v-model="add.sale"></el-input>
            </div>
            <div class="houseInput">
              <label>住房售出状态：</label>
              <el-radio v-model="add.stated" label="0" border size="medium">未售出</el-radio>
              <el-radio v-model="add.stated" label="1" border size="medium">已售出</el-radio>
            </div>
            <div class="houseInput">
              <label>住房户型：</label>
              <el-select v-model="value1" clearable placeholder="--------">
                <el-option
                  v-for="item in house_type"
                  :key="item.value1"
                  :label="item.label1"
                  :value="item.label1">
                </el-option>
              </el-select>
            </div>
            <div class="houseInput">
              <label>住房所在单元：</label>
              <el-select v-model="value2" clearable placeholder="--------">
                <el-option
                  v-for="item in uni"
                  :key="item.value2"
                  :label="item.label2"
                  :value="item.label2">
                </el-option>
              </el-select>
            </div>
            <div class="houseInput">
              <label>住房所在楼栋：</label>
              <el-select v-model="id" clearable placeholder="--------">
                <el-option
                  v-for="item in building"
                  :key="item.id"
                  :label="item.name"
                  :value="item.name">
                </el-option>
              </el-select>
            </div>
          </div>
          <div>
            <el-button type="primary" size="mini" @click="submit">添加</el-button>
          </div>
        </div>
        <div class="inputHouse" v-else>
          <div class="houseEntry">
            <div class="houseInput">
              <label>房号：</label>
              <el-input size="small" v-model="info.house_id"></el-input>
            </div>
            <div class="houseInput">
              <label>占地面积(m²)：</label>
              <el-input size="small" v-model="info.area"></el-input>
            </div>
            <div class="houseInput">
              <label>户主id：</label>
              <el-input size="small" v-model="info.household"></el-input>
            </div>
            <div class="houseInput">
              <label>售价(元/m²)</label>
              <el-input size="small" v-model="info.sale"></el-input>
            </div>
            <div class="houseInput">
              <label>住房售出状态：</label>
              <el-checkbox v-model="info.stated">售出</el-checkbox>
            </div>
            <div class="houseInput">
              <label>住房户型：</label>
              <el-select v-model="value1" clearable placeholder="--------">
                <el-option
                  v-for="item in house_type"
                  :key="item.value1"
                  :label="item.label1"
                  :value="item.label1">
                </el-option>
              </el-select>
            </div>
            <div class="houseInput">
              <label>住房所在单元：</label>
              <el-select v-model="value2" clearable placeholder="--------">
                <el-option
                  v-for="item in uni"
                  :key="item.value2"
                  :label="item.label2"
                  :value="item.value2">
                </el-option>
              </el-select>
            </div>
            <div class="houseInput">
              <label>住房所在楼栋：</label>
              <el-select v-model="id" clearable placeholder="--------">
                <el-option
                  v-for="item in building"
                  :key="item.id"
                  :label="item.name"
                  :value="item.name">
                </el-option>
              </el-select>
            </div>
          </div>
          <div class="submit_bottom">
            <el-button class="el-icon-arrow-left" size="small" @click="goBack">返回</el-button>
            <el-button class="el-icon-delete" size="small" type="danger">删除</el-button>
            <el-button size="small" type="primary" @click="houseSave">保存</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </el-col>
</template>

<script>
export default {
  inject: ['reload'],
  name: "houseManagement",
  data() {
    return {
      house_type: [
        {value1: '0', label1: '两房一厅'},
        {value1: '1', label1: '三房一厅'},
        {value1: '2', label1: '四房一厅'},
        {value1: '3', label1: '四房两厅'}
      ],
      uni: [
        {value2: '0', label2: '一单元'},
        {value2: '1', label2: '二单元'},
        {value2: '2', label2: '三单元'}
      ],
      building: '',
      value1: '',
      value2: '',
      id: '',
      total: 0,
      tableData: [],
      addHouse: 0,
      content: "添加住房",
      flag: 0,
      add: {
        house_id: '',
        area: '',
        sale: '',
        stated: '',
        household: '',
      },
      info: {
        house_id: '',
        house_type: '',
        area: '',
        sale: '',
        stated: '',
        household: '',
        uni: '',
        building: ''
      },
      filters: {
        size: 5,   //单页显示条数
        page: 1,   //当前页码
      },
      searchWord: '',
    }
  },
  created() {
    this.getHouse();
  },
  methods: {
    filterTag(value, row) {
      return row.stated === value;
    },
    submit() {
      this.$axios.post(`${this.$settings.HOST}/build/House/`, {
        info: this.add,
        house_type: this.value1,
        uni: this.value2,
        building: this.id,
      }).then(response => {
        this.$message.success(response.data.msg);
        this.add = '';
        this.value1 = this.value2 = this.id = '';
      }).catch(error => {
        console.log(error.response.data);
      });
    },
    deleteHouse(row) {
      this.$axios.delete(`${this.$settings.HOST}/build/House/`, {
        params: {
          hid: row.id,
        },
      }).then(response => {
        this.$message.success(response.data.msg);
        this.$store.commit("del_house", response.data.length);
        this.reload();
      }).catch(error => {
        this.$message.error(error.response);
      });
    },
    handleClick(row) {
      sessionStorage.hhid = row.id;
      this.flag = this.addHouse = 1;
      this.content = '修改住房信息';
      this.getBuildId();
      this.$axios.patch(`${this.$settings.HOST}/build/House/`, {
        hid: row.id,
      }).then(response => {
        this.info = response.data;
        this.info.stated = response.data.stated === 1;
        this.value1 = response.data.house_type;
        this.value2 = response.data.uni;
        this.id = response.data.building;
      }).catch(error => {
        console.log(error.response.data);
      });
    },
    houseSave() {
      this.$axios.put(`${this.$settings.HOST}/build/House/`, {
        data: this.info,
        hid: sessionStorage.getItem('hhid'),
      }).then(response => {
        this.$message.success(response.data.msg);
        this.reload();
      }).catch(error => {
        console.log(error.response);
      });
    },
    getBuildId() {
      this.$axios.get(`${this.$settings.HOST}/build/cateList/`, {}).then(response => {
        this.building = response.data;
      }).catch(error => {
        console.log(error.response.data);
      });
    },
    search() {
      this.$axios.post(`${this.$settings.HOST}/build/search_house/`, {
        key: this.searchWord,
      }).then(response => {
        this.tableData = response.data;
        this.$store.commit("del_house", response.data.length);
        this.$message.success('查找成功');
      }).catch(error => {
        this.$message.error('查找失败');
      });
    },
    goBack() {
      this.addHouse = 0;
      this.reload();
    },
    getHouse() {
      let filters = {
        page: this.filters.page,
        size: this.filters.size,
      };
      this.$axios.get(`${this.$settings.HOST}/build/house/`, {
        params: filters
      }).then(response => {
        this.tableData = response.data.results;
        this.$store.commit("del_house", response.data.count);
        this.total = response.data.count;
      }).catch(error => {
        console.log(error.response);
      });
    },
    handleChange(page) {
      console.log("本次点击的页码:", page);
      this.filters.page = page;
      this.getHouse();
    },
    sizeChange(size) {
      this.filters.size = size;
      this.filters.page = 1;
      this.getHouse();
    },
  }
}
</script>

<style scoped>
.houseManage {
  min-height: 100vh;
  padding: 20px;
  background-color: rgb(241, 241, 241);
}

.houseManage .page_info {
  text-align: center;
}

.houseManage .house_manage {
  min-height: 95vh;
}

.houseManage .house_manage >>> .el-card__body {
  padding: 0;
}

.houseSearch {
  width: auto;
  height: 35px;
  padding: 8px;
  background-color: rgb(248, 248, 248);
  border-bottom: #dcdcdc solid 1px;
}

.houseSearch .el-input {
  width: 240px;
  padding-right: 20px;
}

.houseSearch .add {
  float: right;
}

.showHouse {
  padding: 20px;
}

.showHouse >>> .el-table thead {
  color: rgb(2, 192, 208);
}

.showHouse .el-result {
  padding: 0;
}

.showHouse >>> .el-result__icon svg {
  width: 20px;
  height: 20px;
}

.showHouse i {
  padding-right: 20px;
  cursor: pointer;
}

.showHouse i:hover:nth-child(1) {
  color: rgb(64, 158, 255);
}

.showHouse i:hover:nth-child(2) {
  color: rgb(255, 64, 80);
}

.house_manage p {
  font-size: 10px;
  color: silver;
  padding-left: 10px;
}

.addHouse {
  padding: 20px;
}

.addHouse .el-page-header {
  padding: 10px;
}

.inputHouse .el-button {
  float: right;
  margin-right: 20px;
}

.houseEntry {
  padding: 20px;
  margin-bottom: 10px;
  min-height: 30vh;
}

.houseEntry .subHeader {
  width: auto;
  height: 3vh;
  background-color: #333;
  color: white;
  padding: 5px;
  margin-bottom: 15px;
}

.houseEntry .houseInput {
  padding-bottom: 30px;
}

.houseEntry .el-col {
  padding-bottom: 10px;
}

.houseInput .el-input {
  width: 250px;
}

.houseInput label {
  display: inline-block;
  width: 230px;
  font-weight: bolder;
}

.houseInput p {
  padding-left: 235px;
  color: dimgrey;
}

.submit_bottom {
  width: auto;
  height: 7vh;
  padding: 10px;
}
</style>

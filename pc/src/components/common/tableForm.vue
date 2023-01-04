<template>
  <el-table
      :data="tableData"
      style="width: 100%"
      max-height="770">
    <el-table-column
        fixed
        sortable
        prop="carry_date"
        label="日期"
        width="170">
    </el-table-column>
    <el-table-column
        prop="handler.build_num"
        label="所在楼栋"
        width="100">
    </el-table-column>
    <el-table-column
        prop="handler.rom_num"
        label="房号"
        width="100">
    </el-table-column>
    <el-table-column
        prop="handler.mobile"
        label="联系方式"
        width="180">
    </el-table-column>
    <el-table-column
        prop="content"
        label="内容"
        width="300">
    </el-table-column>
    <el-table-column
        fixed="right"
        label="操作"
        width="120">
      <template slot-scope="scope">
        <el-button
            v-show="scope.row.stated === 0"
            @click.native.prevent="processedRow(scope.row)"
            type="text"
            size="small">
          处理
        </el-button>
        <el-button
            v-show="scope.row.stated === 1"
            @click.native.prevent="processedRow(scope.row)"
            type="text"
            size="small">
          完成
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: "tableForm",
  inject: ['reload'],
  props: ["tableData", "sign"],
  data() {
    return {
      tableData: this.tableData,
    }
  },
  methods: {
    processedRow(row) {
      if (this.sign === 1) {
        this.$axios.post(`${this.$settings.HOST}/equipment/repair/`, {
          rid: row.id,
          stated: row.stated,
          wid: sessionStorage.getItem('user_id'),
        }).then(response => {
          console.log(response.data.msg);
          this.$message.success('处理成功');
          this.reload();
        }).catch(error => {
          console.log(error.response.data);
        });
      } else if (this.sign === 2) {
        this.$axios.post(`${this.$settings.HOST}/communication/complaint/change_stated/`, {
          cid: row.id,
          stated: row.stated,
          wid: sessionStorage.getItem('user_id'),
        }).then(response => {
          console.log(response.data.msg);
          this.$message.success('处理成功');
          this.reload();
        }).catch(error => {
          console.log(error.response.data);
        });
      }

    },
  }
}
</script>

<style scoped>

</style>

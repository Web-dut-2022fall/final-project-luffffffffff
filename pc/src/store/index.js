import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    users_length: 0,
    build_length: 0,
    house_length: 0,
    message_length: 0,
    parking_length: 0,
    equipment_length: 0,
    untreated_repair_length: 0,
    processing_repair_length: 0,
    processed_repair_length: 0,
    untreated_complaint_length: 0,
    processing_complaint_length: 0,
    processed_complaint_length: 0,
  },
  mutations: {
    del_user(state, length,) {
      state.users_length = length;
    },
    del_build(state, length,) {
      state.build_length = length;
    },
    del_house(state, length,) {
      state.house_length = length;
    },
    del_parking(state, length,) {
      state.parking_length = length;
    },
    del_equipment(state, length,) {
      state.equipment_length = length;
    },
    show_msg(state, length,) {
      state.message_length = length;
    },
    show_untreated_repair(state, length,) {
      state.untreated_repair_length = length;
    },
    show_processing_repair(state, length,) {
      state.processing_repair_length = length;
    },
    show_processed_repair(state, length,) {
      state.processed_repair_length = length;
    },
    show_untreated_complaint(state, length,) {
      state.untreated_complaint_length = length;
    },
    show_processing_complaint(state, length,) {
      state.processing_complaint_length = length;
    },
    show_processed_complaint(state, length,) {
      state.processed_complaint_length = length;
    }
  },
})

<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import HelloWorld from "./components/HelloWorld.vue";
import type { Student, StudentCreate } from "./types";
import { onMounted, ref } from "vue";
import {
  createStudent,
  deleteStudent,
  getStudent,
  getStudentByName,
  getStudents,
  updateStudent,
} from "./services/studentService";
import { ElMessage } from "element-plus";

const student = ref<Student | null>(null);
const students = ref<Student[] | null>(null);
const studentForm = ref<StudentCreate>({
  student_id: 0,
  name: "",
  major: "",
  status: "",
});

const stutas = [
  { label: "在读", value: "在读" },
  { label: "毕业", value: "毕业" },
  { label: "休学", value: "休学" },
];

const majors = [
  { label: "计算机", value: "计算机" },
  { label: "数学", value: "数学" },
  { label: "物理", value: "物理" },
];

onMounted(async () => {
  students.value = await getStudents();
});

function genRandID() {
  return Math.floor(Math.random() * 1000000);
}

async function handleSubmit() {
  try {
    if (studentForm.value.name === "") {
      ElMessage.error("name is required");
      return;
    }
    studentForm.value.student_id = genRandID();
    await createStudent(studentForm.value);
    studentForm.value = {
      student_id: 0,
      name: "",
      major: "",
      status: "",
    };
    students.value = await getStudents();
  } catch (error) {
    console.error(error);
  }
}

async function handleDeleate(id: number) {
  try {
    await deleteStudent(id);
    students.value = await getStudents();
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <div class="margin_both">
    <el-card class="margin_bottom">
      <el-form :model="studentForm" label-width="auto">
        <el-row justify="start" :gutter="10">
          <el-col :span="7">
            <el-form-item label="Name">
              <el-input
                v-model="studentForm.name"
                placeholder="name"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item label="Major">
              <el-select
                v-model="studentForm.major"
                size="middle"
                placeholder="major"
                clearable
              >
                <el-option
                  v-for="item in majors"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item label="Status">
              <el-select
                v-model="studentForm.status"
                size="middle"
                placeholder="status"
                clearable
              >
                <el-option
                  v-for="item in stutas"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="3">
            <el-button type="primary" @click="handleSubmit"> submit </el-button>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    <el-card>
      <el-table :data="students" style="width: 100%">
        <el-table-column label="id" prop="student_id" />
        <el-table-column label="name" prop="name" />
        <el-table-column label="major" prop="major" />
        <el-table-column label="status" prop="status" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="{ row }">
            <el-button type="primary" @click="handleUpdate(row.student_id)"
              >修改</el-button
            >
            <el-button type="danger" @click="handleDeleate(row.student_id)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.margin_both {
  margin: auto 20px;
}

.margin_bottom {
  margin-bottom: 10px;
}
</style>

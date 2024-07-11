import apiClient from './apiClient'
import type { Student, StudentCreate, StudentUpdate } from '../types'

export const createStudent = async (data: StudentCreate): Promise<Student> => {
    const response = await apiClient.post<Student>('/students/', data)
    return response.data
}

export const deleteStudent = async (student_id: number): Promise<void> => {
    await apiClient.delete(`/students/${student_id}`)
}

export const updateStudent = async (student_id: number, data: StudentUpdate): Promise<Student> => {
    const response = await apiClient.put<Student>(`/students/${student_id}`, data)
    return response.data
}

export const getStudent = async (student_id: number): Promise<Student> => {
    const response = await apiClient.get<Student>(`/students/${student_id}`)
    return response.data
}

export const getStudentByName = async (name: string): Promise<Student[]> => {
    const response = await apiClient.get<Student[]>(`/students?name=${name}`)
    return response.data
}

export const getStudents = async (): Promise<Student[]> => {
    const response = await apiClient.get<Student[]>('/students/')
    return response.data
}


// src/types.ts
export interface StudentBase {
    student_id: number;
    name: string;
    major: string;
    status: string;
}

export interface StudentCreate extends StudentBase { }

export interface StudentUpdate extends Partial<StudentBase> { }

export interface Student extends StudentBase {
    student_id: number;
    created_at: string;
    updated_at: string;
}

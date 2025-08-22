import baseApi from "@/api/base";
import { Category, CategoryQueryFilter, ServerPaginatedResult } from "@/types";

// API functions
export async function getAllCategories(params?: Partial<CategoryQueryFilter>) {
  const res = await baseApi.get<ServerPaginatedResult<Category>>(
    "/admin/products/category/",
    { params },
  );
  return res.data;
}

export async function getCategory(id: string) {
  const res = await baseApi.get<Category>(`/admin/products/category/${id}/`);
  return res.data;
}

export async function createCategory(data: FormData) {
  const res = await baseApi.post<Category>(`/admin/products/category/`, data);
  return res.data;
}

export async function updateCategory(data: FormData) {
  const id = data.get("id");
  const res = await baseApi.put<Category>(`/admin/products/category/${id}/`, data);
  return res.data;
}

export async function deleteCategory(id: string | number) {
  const res = await baseApi.delete(`/admin/products/category/${id}/`);
  return res.data;
}

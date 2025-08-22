import baseApi from "@/api/base";
import {
  ServerPaginatedResult,
  StoreItemCreate,
  StoreItemDetails,
  StoreItemQueryFilter,
} from "@/types";

export async function getMyStoreItems(params?: Partial<StoreItemQueryFilter>) {
  return baseApi
    .get<ServerPaginatedResult<StoreItemDetails>>("/stores/store_item/", { params })
    .then((res) => res.data);
}

export async function getMyStoreItem(id: string | number) {
  return baseApi
    .get<StoreItemDetails>(`/stores/store_item/${id}/`)
    .then((res) => res.data);
}
export async function addMyStoreItems(data: StoreItemCreate) {
  return baseApi.post("/stores/store_item/", data).then((res) => res.data);
}

export async function update(data: StoreItemCreate & { id: string | number }) {
  return baseApi
    .put(`/stores/store_item/${data.id}/`, data)
    .then((res) => res.data);
}

export async function deleteMyStoreItems(id: string | number) {
  return baseApi.delete(`/stores/store_item/${id}/`).then((res) => res.data);
}

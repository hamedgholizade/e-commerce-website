import baseApi from "@/api/base";
import { AddressCreateData, AddressType } from "@/types";

export async function createStoreAddress(data: AddressCreateData) {
  const res = await baseApi.post<AddressType>(`/locations/address/`, data);
  return res.data;
}

export async function updateStoreAddress(
  data: AddressCreateData & { id: string | number },
) {
  const res = await baseApi.put<AddressType>(
    `/locations/address/${data.id}/`,
    data,
  );
  return res.data;
}

export async function deleteStoreAddress(addressId: string | number) {
  const res = await baseApi.delete(`/locations/address/${addressId}/`);
  return res.data;
}

export async function getStoreAddress() {
  const res = await baseApi.get<AddressType[]>(`/locations/address/`);
  return res.data;
}

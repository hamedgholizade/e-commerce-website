import baseApi from "../base";
import { CartItem, MyCart } from "@/types";

export const getUserCart = async () => {
  const res = await baseApi<MyCart>("/carts/cart/");
  return res.data;
};
export const getUserCartItems = async () => {
  const res = await baseApi<CartItem[]>("/carts/items/");
  return res.data;
};
export const addProductToCart = async (id: number | string) => {
  const res = await baseApi.post(`/carts/add_to_cart/${id}/`);
  return res.data;
};

export const updateCartItemQuantity = async (
  id: number | string,
  quantity: number,
) => {
  const res = await baseApi.patch(`/carts/items/${id}/`, {
    quantity,
  });
  return res.data;
};

export const removeCartItem = async (id: number | string) => {
  const res = await baseApi.delete(`/carts/items/${id}/`);
  return res.data;
};

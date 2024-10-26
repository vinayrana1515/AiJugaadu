import { createApi } from "@reduxjs/toolkit/query";
import { apiSlice } from "./apiSlice";
const ProductURL = "http://127.0.0.1:5001/data";
export const productSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getProducts: builder.query({
      query: () => ({
        url: ProductURL,
      }),
      keepUnusedDataFor: 5,
    }),
  }),
});
export const { useGetProductsQuery } = productSlice;

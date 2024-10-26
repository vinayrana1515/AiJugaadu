import React from "react";
import Product from "../components/Product";
import { Row, Col } from "react-bootstrap";
import { useEffect, useState } from "react";
import axios from "axios";
import { useGetProductsQuery } from "../slices/productSlice";

const HomeScreen = () => {
  //const { data: products, isLoading, isError } = useGetProductsQuery();
  // console.log(products);

  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      const response = await axios.get("http://127.0.0.1:5001/data");
      setProducts(response.data);
    };
    fetchProducts();
  }, []);

  return (
    <>
      <h1>Products</h1>
      <Row>
        {products.map((product) => (
          <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
            <Product product={product} />
          </Col>
        ))}
      </Row>
    </>
  );
};

export default HomeScreen;

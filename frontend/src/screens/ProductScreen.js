import React from "react";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";
import {
  Row,
  Col,
  Image,
  ListGroup,
  Card,
  Button,
  Form,
  ListGroupItem,
} from "react-bootstrap";
import Rating from "../components/Rating";
import axios from "axios";
import ChatBot from "../components/ChatBot";

const ProductScreen = () => {
  const [product, setProduct] = useState({});
  const { id: productId } = useParams();

  const [showChatBot, setShowChatBot] = useState(false);

  //const product = products.find((p) => p._id === productId);
  useEffect(() => {
    const fetchProduct = async () => {
      const response = await axios.get(
        `http://127.0.0.1:5000/data/${productId}`
      );
      setProduct(response.data);
    };
    fetchProduct();
  }, [productId]);

  const handleNegotiateClick = () => {
    setShowChatBot(true); // Show the chat bot when button is clicked
  };

  const handleCloseChatBot = () => {
    setShowChatBot(false); // Hide the chat bot when close is clicked
  };
  return (
    <>
      <Link className='btn btn-light my-3' to='/'>
        Go Back
      </Link>
      <Row>
        <Col md={5}>
          <Image src={product.image} alt={product.name} fluid />
        </Col>
        <Col md={4}>
          <ListGroup variant='flush'>
            <ListGroupItem>
              <h3>{product.name}</h3>
            </ListGroupItem>
            <ListGroupItem>
              <Rating
                value={product.rating}
                text={`${product.numreviews} reviews`}
              />
            </ListGroupItem>
            <ListGroupItem>Price :${product.price}</ListGroupItem>
            <ListGroupItem>{product.description}</ListGroupItem>
          </ListGroup>
        </Col>
        <Col md={3}>
          <Card>
            <ListGroup variant='flush'>
              <ListGroupItem>
                <Row>
                  <Col>Price:</Col>
                  <Col>
                    <strong>${product.price}</strong>
                  </Col>
                </Row>
              </ListGroupItem>
              <ListGroupItem>
                <Row>
                  <Col>Status:</Col>
                  <Col>
                    <strong>
                      {product.countinstock > 0 ? "In Stock" : "Out of Stock"}
                    </strong>
                  </Col>
                </Row>
              </ListGroupItem>
              <ListGroupItem>
                <Row>
                  <Col>
                    <Button
                      className='btn-block'
                      type='button'
                      disabled={product.countinstock === 0}
                    >
                      Add To Cart
                    </Button>
                  </Col>
                  <Col>
                    <Button
                      className='btn-block'
                      type='button'
                      disabled={product.countinstock === 0}
                      onClick={handleNegotiateClick} // Open chat bot on click
                    >
                      Negotiate
                    </Button>
                    {/* <Button
                      className='btn-block'
                      type='button'
                      disabled={product.countInStock === 0}
                    >
                      Negotiate
                    </Button> */}
                  </Col>
                </Row>
              </ListGroupItem>
            </ListGroup>
          </Card>
        </Col>
      </Row>
      {showChatBot && (
        <ChatBot onClose={handleCloseChatBot} productId={productId} />
      )}
    </>
  );
};

export default ProductScreen;

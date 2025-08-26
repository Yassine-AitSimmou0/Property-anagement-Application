import React, { useState } from "react";
import { addProperty, Property, updateProperty } from "../services/api";
import { TextField, Button, Box } from "@mui/material";

const AddProperty = ({
  handleClose,
  _property,
}: {
  handleClose: () => void;
  _property?: Property;
}) => {
  const [property, setProperty] = useState({
    name: "",
    address: "",
    type: "",
    number_of_units: 0,
    rental_cost: 0,
    ..._property,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProperty({ ...property, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      _property ?
        updateProperty({
          ...property,
          id: _property.id,
          number_of_units: parseInt(property.number_of_units as any),
          rental_cost: parseInt(property.rental_cost as any),
        }).then((data) => {
          if (data) handleClose();
          console.log(data);
        })
        : addProperty({
          ...property,
          number_of_units: parseInt(property.number_of_units as any),
          rental_cost: parseInt(property.rental_cost as any),
        }).then((data) => {
          if (data) handleClose();
          console.log(data);
        });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <TextField
        name="name"
        label="Property Name"
        value={property.name}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        name="address"
        label="Address"
        value={property.address}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        name="type"
        label="Type"
        value={property.type}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        name="number_of_units"
        label="Number of Units"
        value={property.number_of_units}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        name="rental_cost"
        label="Rental Cost"
        value={property.rental_cost}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: 2,
        }}
      >
        <Button type="submit" variant="contained" color="primary">
          {
            _property
              ? "Update"
              : "Add"
          } Property
        </Button>
        <Button variant="text" color="error" onClick={handleClose}>
          Cancel
        </Button>
      </Box>
    </Box>
  );
};

export default AddProperty;

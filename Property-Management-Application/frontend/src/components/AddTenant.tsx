import React, { useState } from "react";
import { addTenant, Property, Tenant, updateTenant } from "../services/api";
import { TextField, Button, Box, Modal } from "@mui/material";
import PropertyList from "./PropertyList";
import { Card, CardContent, Typography, Grid } from '@mui/material';

const PropertyCard: React.FC<Property> = ({
  name,
  address,
  type,
  number_of_units,
  rental_cost,
  created_at,
  updated_at,
}) => {
  return (
    <Card sx={{ padding: '16px' }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {address}
        </Typography>
        <Grid container spacing={2} sx={{ marginTop: '12px' }}>
          <Grid item xs={6}>
            <Typography variant="body1">
              <strong>Type:</strong> {type}
            </Typography>
            <Typography variant="body1">
              <strong>Units:</strong> {number_of_units}
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body1">
              <strong>Cost:</strong> ${rental_cost.toFixed(2)}
            </Typography>
            <Typography variant="body1">
              <strong>Created:</strong> {new Date(created_at).toLocaleDateString()}
            </Typography>
            <Typography variant="body1">
              <strong>Updated:</strong> {new Date(updated_at).toLocaleDateString()}
            </Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

const AddTenant = ({ handleClose, _tenant }: {
  handleClose: () => void;

  _tenant?: Tenant;
}) => {
  const [tenant, setTenant] = useState({
    id: -1,
    name: "",
    email: "",
    property_id: -1,
    ..._tenant,
  });
  const [open, setOpen] = useState(false);
  const [selectedProperty, setSelectedProperty] = useState(-1);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTenant({ ...tenant, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    _tenant
      ? updateTenant(tenant).then(() => {
        handleClose();
      })
      : addTenant(tenant).then(() => {
        handleClose();
      })

  };



  return (
    <Box component="form" onSubmit={handleSubmit} sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '16px',
    }}>
      <TextField
        name="name"
        label="Tenant Name"
        value={tenant.name}
        onChange={handleChange}
        fullWidth

      />
      <TextField
        name="email"
        label="email"
        value={tenant.email}
        onChange={handleChange}
        fullWidth

      />

      {
        tenant.property && (
          <PropertyCard
            id={tenant.property.id}
            name={tenant.property.name}
            address={tenant.property.address}
            type={tenant.property.type}
            number_of_units={tenant.property.number_of_units}
            rental_cost={tenant.property.rental_cost}
            created_at={tenant.property.created_at}
            updated_at={tenant.property.updated_at}
          />
        )
      }

      <Button variant="contained" onClick={() => setOpen(true)} sx={{

      }}>
        Select Property
      </Button>

      <Modal open={open} onClose={() => setOpen(false)}>
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "#fff",
            padding: 4,
            borderRadius: 4,
            width: "80%",
            gap: 2,
          }}
        >
          <PropertyList
            setSelectedProperty={setSelectedProperty}
            selectedProperty={selectedProperty}
          />
          <Button
            sx={{
              marginTop: 2,
            }}
            variant="contained"
            color="primary"
            onClick={() => {
              setTenant({ ...tenant, property_id: selectedProperty });
              setOpen(false);
            }}
          >
            Confirm
          </Button>
        </Box>
      </Modal>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          width: "100%",
        }}
      >
        <Button type="submit" variant="contained" color="primary">
          {
            _tenant ? "Update" : "Add"
          } Tenant
        </Button>
        <Button variant="text" color="error" onClick={handleClose}>
          Cancel
        </Button>
      </Box>
    </Box>
  );
};

export default AddTenant;

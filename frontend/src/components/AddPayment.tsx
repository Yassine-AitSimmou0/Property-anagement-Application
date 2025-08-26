import React, { useState } from "react";
import { addPayment, Payment } from "../services/api";
import { TextField, Button, Box } from "@mui/material";

const AddPayment = ({ _payment }: { _payment: Payment }) => {
  const [payment, setPayment] = useState({
    tenant_id: -1,
    amount: 0,
    date: "",
    status: "",
    settled: false,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPayment({ ...payment, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    addPayment(payment).then(() => {
      // Optionally, clear the form or show a success message
    });
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <TextField
        name="tenantId"
        label="Tenant ID"
        value={payment.tenant_id}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        name="amount"
        label="Amount"
        value={payment.amount}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        name="date"
        label="Date"
        value={payment.date}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        name="status"
        label="Status"
        value={payment.status}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <Button type="submit" variant="contained" color="primary">
        Add Payment
      </Button>
    </Box>
  );
};

export default AddPayment;

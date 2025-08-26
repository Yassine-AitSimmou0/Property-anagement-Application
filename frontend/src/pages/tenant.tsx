import React, { useState } from "react";
import TenantList from "./../components/TenantList";
import AddTenant from "./../components/AddTenant";
import {
  Box, Container, Modal
} from "@mui/material";
import SpeedDial from "@mui/material/SpeedDial";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import SpeedDialIcon from "@mui/material/SpeedDialIcon";
import AddIcon from "@mui/icons-material/Add";
import "react-toastify/dist/ReactToastify.css";
import {
  Tenant,
} from "./../services/api";

const TenantPage = () => {
  const [open, setOpen] = React.useState(false);
  const [tenant, setTenant] = useState<Tenant>();

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Container maxWidth="lg">
      <TenantList open={open} setTenant={setTenant} setOpen={setOpen} />
      <Modal open={open} onClose={handleClose}>
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "#fff",
            padding: 4,
            borderRadius: 4,
          }}
        >
          <AddTenant handleClose={handleClose} _tenant={tenant} />
        </Box>
      </Modal>
      <SpeedDial
        ariaLabel="SpeedDial basic example"
        sx={{ position: "fixed", bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
      >
        <SpeedDialAction
          key="Add Tenant"
          icon={<AddIcon />}
          tooltipTitle="Add Tenant"
          onClick={() => setOpen(true)}
        />
      </SpeedDial>
    </Container>
  );
};

export default TenantPage;

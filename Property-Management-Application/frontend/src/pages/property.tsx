import React, { useState } from "react";
import PropertyList from "./../components/PropertyList";
import AddProperty from "./../components/AddProperty";
import {
  Box, Container, Modal
} from "@mui/material";
import SpeedDial from "@mui/material/SpeedDial";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import SpeedDialIcon from "@mui/material/SpeedDialIcon";
import AddIcon from "@mui/icons-material/Add";
import "react-toastify/dist/ReactToastify.css";
import {
  Property
} from "./../services/api";

const PropertyPage = () => {
  const [open, setOpen] = React.useState(false);
  const [property, setProperty] = useState<Property>();



  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Container maxWidth="lg">
      <PropertyList
        sx={{
          maxHeight: "none",
        }}
        open={open}
        setOpen={setOpen}
        Property={property}
        setProperty={setProperty}
      />
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
          <AddProperty handleClose={handleClose} _property={property} />
        </Box>
      </Modal>
      <SpeedDial
        ariaLabel="SpeedDial basic example"
        sx={{ position: "fixed", bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
      >
        <SpeedDialAction
          key="Add Payment"
          icon={<AddIcon />}
          tooltipTitle="Add Payment"
          onClick={() => setOpen(true)}
        />
      </SpeedDial>
    </Container>
  );
};

export default PropertyPage;

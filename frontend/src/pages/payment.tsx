import PaymentList from "./../components/PaymentList";
import {
  Container
} from "@mui/material";
import SpeedDial from "@mui/material/SpeedDial";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import SpeedDialIcon from "@mui/material/SpeedDialIcon";
import AddIcon from "@mui/icons-material/Add";
import "react-toastify/dist/ReactToastify.css";

const PaymentPage = () => {


  return (
    <Container maxWidth="lg">
      <PaymentList />
      <SpeedDial
        ariaLabel="SpeedDial basic example"
        sx={{ position: "fixed", bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
      >
        <SpeedDialAction
          key="Add Payment"
          icon={<AddIcon />}
          tooltipTitle="Add Payment"
          onClick={() => console.log("Add Payment")}
        />
      </SpeedDial>
    </Container>
  );
};

export default PaymentPage;

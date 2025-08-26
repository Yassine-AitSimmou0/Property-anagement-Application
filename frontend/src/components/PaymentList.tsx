import {
  deletePayment,
  fetcher, Payment, setPaymentAsSettled
} from "../services/api";
import {
  Typography, Box,
  Button,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableBody,
  TableCell
} from "@mui/material";
import useSWR from "swr";
import Loading from "./spinner";

const PaymentList = () => {

  const { data: payments, isLoading, mutate } = useSWR<Payment[]>('/payments', fetcher, {
    revalidateOnFocus: false,
    // retryon error
    errorRetryCount: 0,
    shouldRetryOnError: false

  })


  if (isLoading) {
    return <Loading sx={{
      maxHeight: "300px",
    }} />
  }

  return (
    <>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h4" gutterBottom>
          Payment Management
        </Typography>
      </Box>
      <Paper
        elevation={3}
        sx={{
          maxHeight: "300px",
          overflowY: "auto",
        }}
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Tenant</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Date Paid</TableCell>
              <TableCell>Settled</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {payments && payments.map((payment) => {

              return (
                <TableRow key={payment.id}>
                  <TableCell>{payment.tenant.name}</TableCell>
                  <TableCell>{payment.amount}</TableCell>
                  <TableCell>
                    {new Date(payment.date).toLocaleDateString()}
                  </TableCell>
                  <TableCell>{payment.settled ? "Yes" : "No"}</TableCell>
                  <TableCell
                    sx={{
                      display: "flex",
                      gap: 2,
                    }}
                  >
                    <Button
                      disabled={payment.settled}
                      variant="outlined"
                      color="primary"
                      size="small"
                      onClick={async () => {
                        await setPaymentAsSettled(payment);
                        await mutate();
                      }}
                    >
                      Mark as Settled
                    </Button>
                    <Button
                      variant="outlined"
                      color="secondary"
                      size="small"
                      onClick={async () => {
                        await deletePayment(payment.id);
                        await mutate();
                      }}
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
            {(!payments || !payments.length) && !isLoading && (
              <TableRow >
                <TableCell colSpan={5} >
                  No payments found. Click on the Add Payment button to add a
                  payment.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </Paper>
    </>
  );
};

export default PaymentList;

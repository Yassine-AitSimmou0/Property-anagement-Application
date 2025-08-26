import { useEffect } from "react";
import { deleteTenant, fetcher, Tenant } from "../services/api";
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

const TenantList = ({
  setTenant,
  setOpen,
  open,
}: {
  tenant?: Tenant;
  setTenant?: (tenant: Tenant) => void;
  setOpen?: (open: boolean) => void;
  open?: boolean;
}) => {
  const { data: tenants, isLoading, mutate } = useSWR<Tenant[]>('/tenants', fetcher, {
    revalidateOnFocus: false,
    // retryon error
    errorRetryCount: 0,
    shouldRetryOnError: false
  })

  useEffect(() => {
    (async () => {
      await mutate()
    })();
  }, [open, mutate]);
  if (isLoading) {
    return <Loading sx={{
      maxHeight: "300px",
    }} />
  }
  return (
    <>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h4" gutterBottom>
          Tenant Management
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
              <TableCell>Name</TableCell>
              <TableCell>Contact Details</TableCell>
              <TableCell>Property</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tenants && tenants.map((tenant) => (
              <TableRow key={tenant.id}>
                <TableCell>{tenant.name}</TableCell>
                <TableCell>{tenant.email}</TableCell>
                <TableCell>{tenant?.property?.name}</TableCell>
                <TableCell
                  sx={{
                    display: "flex",
                    gap: 2,
                  }}
                >
                  <Button variant="outlined"
                    href={!setOpen ? `/tenants/` : undefined}

                    color="primary" size="small" onClick={() => {
                      setTenant && setTenant(tenant);
                      setOpen && setOpen(true);
                    }}>
                    Edit
                  </Button>
                  <Button
                    variant="outlined"
                    color="secondary"
                    size="small"
                    onClick={async () => {
                      await deleteTenant(tenant.id);
                      await mutate();
                    }}
                  >
                    Remove
                  </Button>
                </TableCell>
              </TableRow>
            ))}
            {(!tenants || !tenants.length) && !isLoading && (
              <TableRow >
                <TableCell colSpan={5} >
                  No tenants found. Click on the Add tenant button to add a
                  tenant.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </Paper>
    </>
  );
};

export default TenantList;

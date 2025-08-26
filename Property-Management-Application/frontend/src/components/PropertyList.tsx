import { useEffect, } from "react";
import { deleteProperty, fetcher, Property } from "../services/api";
import Checkbox from "@mui/material/Checkbox";
import {
  Typography,

  Box,
  Button,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableBody,
  TableCell,
} from "@mui/material";
import useSWR from "swr";
import Loading from "./spinner";

const PropertyList = ({
  setSelectedProperty,
  selectedProperty,
  sx,
  setProperty,
  setOpen,
  open
}: {
  setSelectedProperty?: (propertyId: number) => void;
  selectedProperty?: number;
  setOpen?: (open: boolean) => void;
  sx?: {
    [key: string]: unknown
  };
  Property?: Property;
  open?: boolean;
  setProperty?: (property: Property) => void;
}) => {
  const { data: properties, isLoading, mutate } = useSWR<Property[]>('/properties', fetcher, {
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
          Property Management
        </Typography>
      </Box>
      <Paper
        elevation={3}
        sx={{
          maxHeight: "300px",
          overflowY: "auto",
          ...sx,
        }}
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Address</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Units</TableCell>
              <TableCell>Rental Cost</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {properties && properties.map((property) => (
              <TableRow key={property.id}>
                <TableCell>{property.name}</TableCell>
                <TableCell>{property.address}</TableCell>
                <TableCell>{property.type}</TableCell>
                <TableCell>{property.number_of_units}</TableCell>
                <TableCell>{property.rental_cost}</TableCell>
                <TableCell
                  sx={{
                    display: "flex",
                    gap: 2,
                  }}
                >
                  <Button
                    variant="outlined"
                    color="primary"
                    size="small"
                    href={!setOpen ? `/properties/` : undefined}
                    onClick={() => {
                      if (setProperty && setOpen) {
                        setProperty(property);
                        setOpen(true);
                      }
                    }}
                  >
                    Edit
                  </Button>
                  <Button
                    variant="outlined"
                    color="secondary"
                    size="small"
                    onClick={async () => {
                      await deleteProperty(property.id);
                      await mutate()
                    }}
                  >
                    Delete
                  </Button>
                  {setSelectedProperty && (
                    <Checkbox
                      checked={selectedProperty === property.id}
                      onChange={() => setSelectedProperty(property.id)}
                    />
                  )}
                </TableCell>
              </TableRow>
            ))}
            {(!properties || !properties.length) && !isLoading && (
              <TableRow >
                <TableCell colSpan={5} >
                  No properties found. Click on the Add property button to add a
                  property.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </Paper>
    </>
  );
};

export default PropertyList;

import React, { useState } from "react";
import PropertyList from "./../components/PropertyList";
import TenantList from "./../components/TenantList";
import PaymentList from "./../components/PaymentList";
import {
  Box, Container,
  Grid, Paper, Typography
} from "@mui/material";
import "react-toastify/dist/ReactToastify.css";
import {
  getPayments,
  getProperties,
  getTenants,
  Payment,
  Property,
  Tenant,
} from "./../services/api";
import Loading from "../components/spinner";

const Dashboard = () => {
  const [activities, setActivities] = useState<string[]>([]);
  const [stats, setStats] = useState({
    properties: 0,
    tenants: 0,
    outstadingPayments: 0,
  });

  const [isLoading, setIsLoading] = useState(true);

  React.useEffect(() => {
    (async () => {
      try {
        const tenants: Tenant[] = (await getTenants())?.data;
        const payments: Payment[] = (await getPayments())?.data;
        const properties: Property[] = (await getProperties())?.data;

        if (!tenants || !payments || !properties) {
          return
        }

        setStats({
          properties: properties.length,
          tenants: tenants.length,
          outstadingPayments: payments.reduce(
            (total, payment) => total + payment.amount,
            0,
          ),
        });

        const activitiesWithTimestamps: {
          message: string;
          timestamp: number;
        }[] = [];

        // Extract data and format messages with timestamps
        tenants.forEach((tenant) =>
          activitiesWithTimestamps.push({
            message: `Tenant ${tenant.name} added to ${tenant?.property?.name}`,
            timestamp: new Date(tenant.created_at).getTime(), // Add actual timestamp if available
          }),
        );
        properties.forEach((property) =>
          activitiesWithTimestamps.push({
            message: `Property ${property.name} added`,
            timestamp: new Date(property.created_at).getTime(), // Add actual timestamp if available
          }),
        );
        payments.forEach((payment) =>
          activitiesWithTimestamps.push({
            message: `Payment of $${payment.amount} received from ${payment.tenant.name}`,
            timestamp: new Date(payment.created_at).getTime(), // Add actual timestamp if available
          }),
        );

        // Sort activities by timestamp most recent first
        activitiesWithTimestamps.sort((a, b) => b.timestamp - a.timestamp);

        // Extract the sorted messages
        let sortedActivities = activitiesWithTimestamps.map(
          (activity) => activity.message,
        );

        // limit to 20 activities
        sortedActivities = sortedActivities.slice(0, 20);

        setActivities(sortedActivities);
      } catch (error) {
        console.error("Error fetching recent activities:", error);
      } finally {
        setIsLoading(false);
      }
    })();
  }, []);

  return (
    <Container maxWidth="lg">
      <Grid container spacing={3}>
        {/* Property Summary */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Total Properties</Typography>
            <Typography variant="h4">{stats.properties}</Typography>
          </Paper>
        </Grid>
        {/* Tenant Summary */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Total Tenants</Typography>
            <Typography variant="h4">{stats.tenants}</Typography>
          </Paper>
        </Grid>
        {/* Payments Summary */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Outstanding Payments</Typography>
            <Typography variant="h4">${stats.outstadingPayments}</Typography>
          </Paper>
        </Grid>
      </Grid>
      <Box mt={4}>
        <Typography variant="h4" gutterBottom>
          Recent Activities
        </Typography>

        <Paper
          elevation={3}
          sx={{
            maxHeight: "300px",
            minHeight: "200px",
            overflowY: "auto",
            padding: 2,
          }}
        >
          {isLoading ? <Loading sx={{
            maxHeight: "200px",
          }} /> :
            activities.length ? (activities.map((activity, index) => (
              <Typography variant="body1" key={index}>
                {activity}
              </Typography>
            ))) : <Box sx={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              height: "100%",
            }}>
              <Typography variant="body1">No recent activities</Typography>
            </Box>
          }
        </Paper>
      </Box>
      <Box mt={4}>
        <PropertyList />
      </Box>
      <Box mt={4}>
        <TenantList />
      </Box>
      <Box mt={4}>
        <PaymentList />
      </Box>
    </Container>
  );
};

export default Dashboard;

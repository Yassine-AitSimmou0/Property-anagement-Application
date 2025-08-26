import { Box, CircularProgress } from "@mui/material";

function Loading({ sx }: {
    sx?: {
        [key: string]: unknown;
    };
}) {
    return (
        <Box
            sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: "100vh",
                ...sx,
            }}
        >
            <CircularProgress color="secondary" />
        </Box>
    );
}

export default Loading;
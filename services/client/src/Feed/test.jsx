import axios from "axios";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { Feed } from "./Feed.jsx";
import { getTitle } from "./utils.js";

vi.mock("axios");


describe("Feed", () => {

    it("Displays spinner while data is being fetched", async () => {
        const promise = Promise.resolve({data: []});
        axios.get.mockImplementationOnce(() => promise);
        render(<Feed />);
        expect(screen.queryByText(/Cargando/)).toBeInTheDocument();
        await waitFor(async () => await promise);
    })

    it("Displays error when failing to fetch data", async () => {
       const promise = Promise.reject();
       axios.get.mockImplementationOnce(() => promise);

       render(<Feed />);
       try{
           await waitFor(async () => await promise);
       } catch (error) {
           expect(screen.queryByText(/Error/)).toBeInTheDocument();
       }
    });

    it("Displays last alert info when data is successfully fetched", async () => {
        const alert = {
            states: [40],  // CDMX
            region: 41204, // Guerrero
            is_event: false,
            references: [],
            id: "20230525000000-L1H8LO",
            time: "2023-05-25T00:00:00",
        };
        const promise = Promise.resolve({data: alert});
        axios.get.mockImplementationOnce(() => promise);

        render(<Feed />);
        await waitFor(async () => await promise);

        expect(screen.queryByText(
            /Alerta en CDMX por sismo en Guerrero/)).toBeInTheDocument();
        expect(screen.queryByText(
            /Mayor/)).toBeInTheDocument();
    });
});

describe("getTitle", () => {
    it("Gets correct title for alerts of single state", () => {
        const cities = [40];
        const region = 41204;
        const time = "2023-05-25T00:00:00";

        const title = getTitle(cities, region, time, false);
        expect(title).toBe("Jueves, 25 de mayo de 2023, 00:00:00 Alerta en CDMX por sismo en Guerrero.");
    });

    it("Gets correct title for alerts of multiple states", () => {
        const cities = [40, 46];
        const region = 41204;
        const time = "2023-05-25T00:00:00";

        const title = getTitle(cities, region, time, false);
        expect(title).toBe("Jueves, 25 de mayo de 2023, 00:00:00 Alerta en CDMX/Puebla por sismo en Guerrero.");
    });

    it("Gets correct title for events", () => {
        const cities = [40];
        const region = 41204;
        const time = "2023-05-25T00:00:00";

        const title = getTitle(cities, region, time, true);
        expect(title).toBe("Jueves, 25 de mayo de 2023, 00:00:00 Sismo en Guerrero.");
    })

});


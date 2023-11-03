import axios from "axios";
import {render, screen, waitFor} from "@testing-library/react";
import {describe, expect, it, vi} from "vitest";
import {HistoryData} from "./History.jsx";
import {historyReducer, HISTORY_ACTIONS} from "./historyReducer.js";
import {AlertTypes, getValidFilters, removeAccents} from "./filters.js";

vi.mock("axios");


describe("HistoryData", () => {
    it("Displays spinner while data is being fetched", () => {
        const promise = Promise.resolve({data: []});
        axios.get.mockImplementationOnce(() => promise);
        render(<HistoryData />);
        expect(screen.queryByText(/Cargando/)).toBeInTheDocument();
    })

    it("Displays error when failing to fetch data", async () => {
        const promise = Promise.reject();
        axios.get.mockImplementationOnce(() => promise);

        render(<HistoryData />);
        try {
            await waitFor(async () => await promise);
        } catch (error) {
            expect(screen.queryByText(/Error/)).toBeInTheDocument();
        }
    });

    it("Displays table after fetching data successfully", async () => {
        const alertData = {
            alerts: [{
                states: [40, 47],  // CDMX
                region: 41201,
                is_event: false,
                references: [],
                id: "20230525000000-L1H8LO",
                time: "2023-05-25T00:00:00",
            },
            {
                states: [46],  // Puebla
                region: 42216,
                is_event: true,
                references: [],
                id: "20230524000000-L2H9LO",
                time: "2023-05-24T12:00:00",
            }],
            count: 2,
            next: null,
            prev: null,
        }
        const promise = Promise.resolve({data: alertData});
        axios.get.mockImplementation(() => promise);

        render(<HistoryData />);

        await waitFor(async () => await promise);

        // One row for the header + 2 of data
        expect(screen.getAllByRole("row").length).toBe(3);
        expect(screen.queryByText(/CDMX, Morelos/)).toBeInTheDocument();
    });

    // TODO: Integration tests for filters
});

describe("historyReducer", () => {

    const initialState = {
        data: {},
        page: 2,
        startDate: null,
        endDate: null,
        isLoading: false,
        isError: false,
        type: AlertTypes.Todos,
        state: null,
        region: null
    }

    it("Setting new page", () => {
        const newState = historyReducer(initialState, {
            type: HISTORY_ACTIONS.SET_PAGE,
            payload: 3
        });
        const expectedState = {
            data: {},
            page: 3,
            startDate: null,
            endDate: null,
            isLoading: false,
            isError: false,
            type: AlertTypes.Todos,
            state: null,
            region: null
        }
        expect(newState).toStrictEqual(expectedState);
    });

    it("Setting new type changes type and resets page", () => {
       const newState = historyReducer(initialState, {
           type: HISTORY_ACTIONS.SET_TYPE,
           payload: AlertTypes.Alerta
       });
       const expectedState = {
           data: {},
           page: 1,
           startDate: null,
           endDate: null,
           isLoading: false,
           isError: false,
           type: AlertTypes.Alerta,
           state: null,
           region: null
       };
       expect(newState).toStrictEqual(expectedState);
    });

    it("Setting state changes state and resets page", () => {
        const state = 40;
        const newState = historyReducer(initialState, {
            type: HISTORY_ACTIONS.SET_STATE,
            payload: state
        });
        const expectedState = {
            data: {},
            page: 1,
            startDate: null,
            endDate: null,
            isLoading: false,
            isError: false,
            type: AlertTypes.Todos,
            state: 40,
            region: null
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Setting region changes region and resets page", () => {
        const newState = historyReducer(initialState, {
           type: HISTORY_ACTIONS.SET_REGION,
           payload: "guerrero"
        });
        const expectedState = {
            data: {},
            page: 1,
            startDate: null,
            endDate: null,
            isLoading: false,
            isError: false,
            type: AlertTypes.Todos,
            state: null,
            region: "guerrero"
        };
        expect(newState).toStrictEqual(expectedState);
    });
});

describe("getFilters", () => {

    it("Only get non null filters", () => {
        const filters = {
            page: 1,
            startDate: null,
            endDate: null,
            type: AlertTypes.Todos,
            state: 40,
            region: "guerrero"
        }
        const valid = getValidFilters(filters);
        const expected = {
            page: 1,
            type: AlertTypes.Todos,
            state: 40,
            region: "guerrero"
        };
        expect(valid).toStrictEqual(expected);
    });

    it("Converts dates to string if present", () => {
        const filters = {
            startDate: new Date(2023, 8, 18, 12, 30, 0, 0),
            endDate: new Date(2023, 8, 19, 12, 30, 0, 0)
        };
        const valid = getValidFilters(filters);
        const expected = {
            start_date: "2023-09-18",
            end_date: "2023-09-19"
        }
        expect(valid).toStrictEqual(expected);
    });
});


describe("removeAccents", () => {

    it("Remove accents from string", () => {
        const withAccents = "hólá wé";
        const noAccents = removeAccents(withAccents);
        const expected = "hola we";
        expect(noAccents).toEqual(expected);
    });

    it("Doesn't alter string without accents", () => {
        const noAccents  = "Pollo Frito";
        const expected = "Pollo Frito";
        expect(removeAccents(noAccents)).toEqual(expected);
    });

});
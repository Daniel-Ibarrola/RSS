import { describe, it, expect } from "vitest";
import { ACTIONS, fetchDataReducer } from "./fetchReducer.js";


describe("fetchDataReducer", () => {
    it("Init fetch sets loading state", () => {
        const initialState = {
            data: [],
            isLoading: false,
            isError: false,
        };
        const newState = fetchDataReducer(initialState,
            {type: ACTIONS.INIT_FETCH});

        const expectedState = {
            data: [],
            isLoading: true,
            isError: false,
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("updates data on successful fetching", () => {
        const alerts = [
            {
                city: 40,  // CDMX
                region: 41201,
                is_event: false,
                references: [],
                id: "20230525000000-L1H8LO",
                time: "2023-05-25T00:00:00",
            },
            {
                city: 46,  // Puebla
                region: 42216,
                is_event: true,
                references: [],
                id: "20230525000000-L1H8LO",
                time: "2023-05-24T12:00:00",
            },
        ];

        const action = { type: ACTIONS.SUCCESS_FETCH, payload: alerts};
        const state = {
            data: [],
            isLoading: true,
            isError: false,
        }
        const newState = fetchDataReducer(state, action);

        const expectedState = {
            data: alerts,  // Stations should be sorted
            isLoading: false,
            isError: false,
        }
        expect(newState).toStrictEqual(expectedState);
    });

    it("sets error state on fetch fail", () => {
        const initialState = {
            data: [],
            isLoading: true,
            isError: false,
        };
        const newState = fetchDataReducer(initialState,
            {type: ACTIONS.FAIL_FETCH});

        const expectedState = {
            data: [],
            isLoading: false,
            isError: true,
        };
        expect(newState).toStrictEqual(expectedState);
    });

});
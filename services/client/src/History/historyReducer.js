import {ACTIONS, fetchDataReducer} from "../shared/index.js";


const numActions = Object.keys(ACTIONS).length;

export const HISTORY_ACTIONS = {
    ...ACTIONS,
    SET_PAGE: numActions + 1,
    SET_TYPE: numActions + 2,
    SET_STATE: numActions + 3,
    SET_REGION: numActions + 4,
    SET_START: numActions + 5,
    SET_END: numActions + 6,
}

export const historyReducer = (state, action) => {
    switch (action.type) {
        case HISTORY_ACTIONS.INIT_FETCH:
        case HISTORY_ACTIONS.SUCCESS_FETCH:
        case HISTORY_ACTIONS.FAIL_FETCH:
                return fetchDataReducer(state, action);
        case HISTORY_ACTIONS.SET_PAGE:
            return {
                ...state,
                page: action.payload,
            };
        case HISTORY_ACTIONS.SET_TYPE:
            return {
                ...state,
                type: action.payload,
                page: 1,
            };
        case HISTORY_ACTIONS.SET_STATE:
            return {
                ...state,
                state: action.payload,
                page: 1,
            };
        case HISTORY_ACTIONS.SET_REGION:
            return {
                ...state,
                region: action.payload,
                page: 1
            };
        case HISTORY_ACTIONS.SET_START:
            return {
                ...state,
                startDate: action.payload,
                page: 1
            };
        case HISTORY_ACTIONS.SET_END:
            return {
                ...state,
                endDate: action.payload,
                page: 1
            }
        default:
            return state;
    }
};


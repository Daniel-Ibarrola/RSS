
export const ACTIONS = {
    INIT_FETCH: 0,
    SUCCESS_FETCH: 1,
    FAIL_FETCH: 2,
};

export const fetchDataReducer = (state, action) => {
    switch (action.type) {
        case ACTIONS.INIT_FETCH:
            return {
                ...state,
                isLoading: true,
                isError: false,
            };
        case ACTIONS.SUCCESS_FETCH:
            return {
                ...state,
                isLoading: false,
                isError: false,
                data: action.payload,
            };
        case ACTIONS.FAIL_FETCH:
            return {
                ...state,
                isLoading: false,
                isError: true,
            };
        default:
            return state;
    }
};

import axios from "axios";
import { ACTIONS } from "./fetchReducer.js";


export const fetchData = async (dispatchFn, url, actions= ACTIONS, params = {}) => {
    dispatchFn({type: actions.INIT_FETCH });
    try {
        const result = await axios.get(url, {params: params});
        dispatchFn({
            type: actions.SUCCESS_FETCH,
            payload: result.data,
        });
    } catch {
        dispatchFn({ type: actions.FAIL_FETCH });
    }
};
import {useState, useEffect} from "react";

export const useHassEntity = <T>(hass: any, entityId: string, initialValue: T, domain: "switch" | "number"): [T, (s: T) => void] => {
    const getHaValue = (): T => {
        if (!hass || !hass.states) return initialValue;
        const stateObj = hass.states[entityId];
        if (!stateObj) return initialValue;
        
        if (domain === "switch") {
            return (stateObj.state === "on") as unknown as T;
        } else if (domain === "number") {
            const val = parseFloat(stateObj.state);
            return (isNaN(val) ? initialValue : val) as unknown as T;
        }
        return initialValue;
    };

    const [storedValue, setStoredValue] = useState<T>(initialValue);

    useEffect(() => {
        const value = getHaValue();
        if (value !== storedValue) {
            setStoredValue(value);
        }
    }, [hass?.states?.[entityId]?.state, domain, entityId]); // eslint-disable-line react-hooks/exhaustive-deps

    const setValue = (value: T) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            
            // We set it locally first to make the UI feel fast and responsive
            setStoredValue(valueToStore);
            
            // Then tell Home Assistant to update
            if (domain === "switch") {
                hass.callService("switch", valueToStore ? "turn_on" : "turn_off", {
                    entity_id: entityId
                });
            } else if (domain === "number") {
                hass.callService("number", "set_value", {
                    entity_id: entityId,
                    value: String(valueToStore)
                });
            }
        } catch (error) {
            console.warn("Failed to set HA entity", error);
        }
    };

    return [storedValue, setValue];
};

import datefns from 'date-fns'


function formatTimestamp(ts, format='YYYY/MM/DD') {
    return datefns.format(datefns.parse(ts), format)
}

export {formatTimestamp}


import { useContext, useState, handleSelect } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import axios from 'axios';
import { Calendar, momentLocalizer } from 'react-big-calendar'
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment'
import '../App.css';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import DeleteIcon from '@mui/icons-material/Delete';
import Divider from '@mui/material/Divider';

const localizer = momentLocalizer(moment)

export default function Events({ }) {
    const [events, setEvents] = useState(null);
    const [selectedEvent, setSelectedEvent] = useState(undefined)
    const [selectedEvents, setSelectedEvents] = useState(undefined)
    const [modalState, setModalState] = useState(false)
    const [selectedDate, setSelectedDate] = useState(undefined)

    function getEvents() {
        axios.get("/events")
            .then(response => {
                console.log("events", response)
                const incomingEvents = response.data.map(({start, end, ...rest}) => {
                    return {
                        start: new Date(Date.parse(start)),
                        end: new Date(Date.parse(end)),
                        ...rest
                       
                    }
                })
                setEvents(incomingEvents)
            })
    }
    const handleSelectedEvent = (event) => {
        setSelectedEvent(event)
        setModalState(true)
        setSelectedEvents(undefined)
    }

    const handleSelectedSlot = (selectedSlot) => {
        setSelectedEvent(undefined)
        setSelectedEvents(undefined)
        console.log("hey")
        const { start, end } = selectedSlot;
        const startDate = new Date(start)
        const endDate = new Date(end)
        console.log(start, end)
        const eventsForThisDay = events.filter(
            event => {
                console.log(new Date(event.start))
                console.log(new Date(event.start).toDateString())
                console.log(startDate.toDateString())
                if (startDate.toDateString() == (new Date(event.start).toDateString()) ||
                    (startDate.toDateString() > (new Date(event.start).toDateString())
                        && endDate.toDateString() < (new Date(event.end).toDateString()))) {
                    return true
                }
            }
        )
        if (eventsForThisDay.length > 0) {
            setSelectedEvents(eventsForThisDay)
            console.log(eventsForThisDay)
            setModalState(true)
            setSelectedDate(startDate.toDateString())
        } else {
            setModalState(false)
        }
    }
    const Modal = () => {
        return (
            <div className={`modal-${modalState == true ? 'show' : 'hide'}`}>
                <Divider sx={{ borderWidth: 5, borderBottomWidth: 5 }} />
                <Box sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '100vw',
                    bgcolor: 'background.paper'
                }}>
                    <List>
                        <Typography variant="h4" align="center">
                            Event: {selectedEvent.title}
                        </Typography>
                        <ListItem  >
                            <Accordion sx={{ width: 1000 }}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls="panel1a-content"
                                    id="panel1a-header"
                                    sx={{ display: "flex" }}
                                >
                                    <Typography align="left" sx={{ width: '100%' }}>{selectedEvent.title}</Typography>
                                    <Button align="right" sx={{ width: '10%' }} variant="outlined" startIcon={<DeleteIcon />} size="small" onClick={() => console.log(selectedEvent)}>
                                        <Typography variant="caption">Delete</Typography>
                                    </Button>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Typography>
                                        {selectedEvent.description}
                                    </Typography>
                                </AccordionDetails>
                            </Accordion>
                        </ListItem>

                    </List>
                </Box>
            </div>
        )
    }
    const MultiEventsModal = () => {
        return (
            <div className={`modal-${modalState == true ? 'show' : 'hide'}`}>
                <Divider sx={{ borderWidth: 5, borderBottomWidth: 5 }} />
                <Box sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '100vw',
                    bgcolor: 'background.paper'
                }}>
                    <List>
                        <Typography variant="h4" align="center">
                            Events For: {selectedDate}
                        </Typography>
                        {selectedEvents.map(selectedEvent => {
                            return (
                                <ListItem  >
                                    <Accordion sx={{ width: 1000 }}>
                                        <AccordionSummary
                                            expandIcon={<ExpandMoreIcon />}
                                            aria-controls="panel1a-content"
                                            id="panel1a-header"
                                            sx={{ display: "flex" }}
                                        >
                                            <Typography align="left" sx={{ width: '100%' }}>{selectedEvent.title}</Typography>
                                            <Button align="right" sx={{ width: '10%' }} variant="outlined" startIcon={<DeleteIcon />} size="small" onClick={() => console.log(selectedEvent)}>
                                                <Typography variant="caption">Delete</Typography>
                                            </Button>
                                        </AccordionSummary>
                                        <AccordionDetails>
                                            <Typography>
                                                {selectedEvent.description}
                                            </Typography>
                                        </AccordionDetails>
                                    </Accordion>
                                </ListItem>
                            )
                        })}
                    </List>
                </Box>
            </div>
        )
    }
    return (
        <Box sx={{ flexGrow: 1 }}>
            {events && events.length > 0 ?
                <div>

                    <Calendar
                        localizer={localizer}
                        events={events}
                        startAccessor="start"
                        endAccessor="end"
                        style={{ height: 500 }}
                        selectable={true}
                        onSelectSlot={(e) => handleSelectedSlot(e)}
                        onSelectEvent={(e) => handleSelectedEvent(e)}
                    // onShowMore={(events, date) => this.setState({ showModal: true, events })}
                    />
                    {selectedEvent && <Modal />}
                    {selectedEvents && <MultiEventsModal />}
                </div> :
                <Button onClick={getEvents} color="inherit">Get Events</Button>
            }
        </Box>
    );
}
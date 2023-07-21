/*
 * Events.js
 * 7/19/2023
 * Ian Percy
 * 
 * 
 * Events view for the application. This will allow users to see their events,
 * search, delete, and add events
 */
import {  useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
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
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import FormControl from '@mui/material/FormControl';
import { subHours } from 'date-fns';

const localizer = momentLocalizer(moment)

export default function Events({ user }) {
    // Set the necessary variables for the class
    // Events is cached and filteredEvents is the working copy of the events list
    const [events, setEvents] = useState([])
    const [filteredEvents, setFilteredEvents] = useState([])
    const [selectedEvent, setSelectedEvent] = useState(undefined)
    const [selectedEvents, setSelectedEvents] = useState(undefined)
    const [modalState, setModalState] = useState(false)
    const [selectedDate, setSelectedDate] = useState(undefined)
    // Variables for the event to add
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const [inputStartDate, setInputStartDate] = useState(undefined)
    const [inputEndDate, setInputEndDate] = useState(undefined)
    const [view, setView] = useState("calendar")

    /*
    * Get all events from the server
    *
    * @param null
    * @return null
    */
    function getEvents() {
        axios.get("/events/" + user.username)
            .then(response => {
                if (response.data !== null && response.data.data !== null) {
                    console.log(response.data, response.data.data)
                    const incomingEvents = response.data.data.map(({ start_date, end_date, ...rest }) => {
                        return {
                            // Need to format to a JS Date object so the calendar works properly
                            startDate: new Date(Date.parse(start_date)),
                            endDate: new Date(Date.parse(end_date)),
                            ...rest

                        }
                    })

                    setEvents(incomingEvents)
                    setFilteredEvents(incomingEvents)
                } else {
                    setEvents(undefined)
                    setFilteredEvents(undefined)
                }
            }).catch(err => {
                console.log(err.response.data);
                window.alert(err.response.data.message)
            })
    }

    /*
    * Handle adding an event
    *
    * @param null
    * @return null
    */
    function handleAddEvent() {
        if (!validate) {
            window.alert("Please enter valid event values")
            return
        }
        axios.post("/events",
            {
                "title": title,
                "description": description,
                "username": user.username,
                "startDate": inputStartDate,
                "endDate": inputEndDate
            })
            .then(response => {
                // console.log("Event added", response)
                getEvents()
                console.log(response)
            }).catch(err => {
                console.log(err.response.data);
                window.alert(err.response.data.message)
            })
    }

    /*
    * Get events on component load
    *
    * @param null
    * @return null
    */
    useEffect(() => {
        getEvents()
    })

    /*
    * Set values for a selected event
    *
    * @param event object to set as the selected event
    * @return null
    */
    const handleSelectedEvent = (event) => {
        setSelectedEvent(event)
        setModalState(true)
        setSelectedEvents(undefined)
    }

    /*
    * Handle filtering events by the "search"dang it
    *
    * @param  e  search page event
    * @return null
    */
    const handleSearch = (e) => {
        if (e.target.value.length < 1)
            setFilteredEvents(events)
        else {
            if (events) {
                let val = events.map(event => {
                    // Check if matches the title or the description
                    if (event.title.indexOf(e.target.value) !== -1 ||
                        event.description.indexOf(e.target.value) !== -1
                    ) {
                        return event
                    }
                    return null
                })
                setFilteredEvents(val)
                setSelectedEvent(undefined)
                setSelectedEvents(undefined)
            }

        }
    }

    /*
    * Handle validate input for event
    *
    * @param null
    * @return null
    */
    function validate() {
        if (!title || title.length > 50 || !description || description.length > 100 ||
            !inputStartDate || !inputEndDate) {
            return false
        }
        return true
    }

    /*
    * Handle event delete
    *
    * @param e page event (to stop the accordion from opening up)
    * @param eventToDelete event object to delete
    * @return null
    */
    const handleDelete = (e, eventToDelete) => {
        e.stopPropagation();
        axios.delete("/events/" + eventToDelete.id)
            .then(() => getEvents())
            .catch(err => {
                console.log(err.response.data);
                window.alert(err.response.data.message)
            })
        // Delete from selected event or selected events
        if (selectedEvent) {
            setSelectedEvent(null)
        }
        if (selectedEvents) {
            let newSelectedEvents = selectedEvents.filter(event => event.title !== eventToDelete.title)
            setSelectedEvents(newSelectedEvents)
        }
    }

    /*
    * Handle choosing a particular slot/date on calendar
    *
    * @param selectedSlot slot to choose as active from the page 
    * @return null
    */
    const handleSelectedSlot = (selectedSlot) => {
        setSelectedEvent(undefined)
        setSelectedEvents(undefined)
        const { start, end } = selectedSlot;
        const startDateRaw = new Date(start)
        const startDate = subHours(startDateRaw, 2).toISOString().split('T')[0]
        const endDateRaw = new Date(end)
        const endDate = subHours(endDateRaw,24 ).toISOString().split('T')[0]
        // Filter events by the date range of the slot
        if (events !== undefined) {
            const eventsForThisDay = events.filter(
                event => {
                    const newEventStartDate = new Date(event.startDate).toISOString().split('T')[0]
                    const newEventEndDate = new Date(event.endDate).toISOString().split('T')[0]
                    console.log(startDate, newEventStartDate)
                    console.log(endDate, newEventEndDate)
                    if (( startDate >= newEventStartDate) && (endDate<= newEventEndDate )) {
                        return true
                    }
                    return false
                }
            )
            // Show views if necessary (slot is not empty)
            if (eventsForThisDay.length > 0) {
                setSelectedEvents(eventsForThisDay)
                setModalState(true)
                setSelectedDate(startDate)
            } else {
                setModalState(false)
            }
        }
    }

    // Modal view for the selected event
    const Modal = () => {
        return (
            <div className={`modal-${modalState === true ? 'show' : 'hide'}`}>
                <Divider sx={{ borderWidth: 5, borderBottomWidth: 5 }} />
                <Box sx={{
                    bgcolor: 'background.paper',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }} width={"98wv"}>
                    <List>
                        <Typography variant="h4" align="center">
                            Event: {selectedEvent.title}
                        </Typography>
                        <ListItem  >
                            <Accordion sx={{ width: "100%" }}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls="panel1a-content"
                                    id="panel1a-header"
                                    sx={{ display: "flex" }}
                                >
                                    <Typography align="left" width={"40vw"}><b>Title:</b> {selectedEvent.title}</Typography>
                                    <Button align="right" variant="outlined" startIcon={<DeleteIcon />} size="small" onClick={e => handleDelete(e, selectedEvent)}>
                                        <Typography variant="caption">Delete</Typography>
                                    </Button>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Typography>
                                        <div>
                                            <Typography>
                                                <b>Description:</b> {selectedEvent.description}
                                            </Typography>
                                            <Typography>
                                                <b>Start:</b> {selectedEvent.startDate.toDateString()} <b>End:</b> {selectedEvent.endDate.toDateString()}
                                            </Typography>
                                        </div>
                                    </Typography>
                                </AccordionDetails>
                            </Accordion>
                        </ListItem>

                    </List>
                </Box>
            </div>
        )
    }

    //Modal view for the selected events
    const MultiEventsModal = () => {
        return (
            <div className={`modal-${modalState === true ? 'show' : 'hide'}`}>
                <Divider sx={{ borderWidth: 5, borderBottomWidth: 5 }} />
                <Box sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    bgcolor: 'background.paper'
                }} width={"98vw"}>
                    <List >
                        <Typography variant="h4" align="center">
                            Events For: {selectedDate}
                        </Typography>
                        {selectedEvents.map(currentEvent => {
                            return (
                                <ListItem >
                                    <Accordion>
                                        <AccordionSummary
                                            expandIcon={<ExpandMoreIcon />}
                                            aria-controls="panel1a-content"
                                            id="panel1a-header"
                                            sx={{ display: "flex" }}
                                        >
                                            <Typography align="left" width={"40vw"}><b>Title:</b> {currentEvent.title}</Typography>
                                            <Button align="right" variant="outlined" startIcon={<DeleteIcon />} size="small" onClick={e => handleDelete(e, currentEvent)}>
                                                <Typography variant="caption">Delete</Typography>
                                            </Button>
                                        </AccordionSummary>
                                        <AccordionDetails>
                                            <div>
                                                <Typography>
                                                    <b>Description:</b> {currentEvent.description}
                                                </Typography>
                                                <Typography>
                                                    <b>Start:</b> {currentEvent.startDate.toDateString()} <b>End:</b> {currentEvent.endDate.toDateString()}
                                                </Typography>
                                            </div>
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
        <Box sx={{ flex: 1 }}>
            <Box >
                <Accordion sx={{ width: "95%vw", display: "flex", height: 70 }}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        display="flex"
                    >
                        <Typography variant="subtitle1" >Search By Title or Description</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <TextField id="standard-basic" label="Search" variant="outlined" sx={{ width: 900, height: 50 }} onChange={(e) => handleSearch(e)} size="small" />
                    </AccordionDetails>
                </Accordion>
                <Accordion sx={{ width: "95%vw", display: "flex", height: 70 }}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        display="flex"
                    >
                        <Typography variant="subtitle1" component="div" >
                            Add Event
                        </Typography>                    </AccordionSummary>
                    <AccordionDetails >

                        <FormControl variant="outlined">
                            <TextField id="title-textfield" label="Title" variant="outlined" value={title} onChange={(e) => setTitle(e.target.value)} size="small" />
                        </FormControl>
                        <FormControl variant="outlined">
                            <TextField id="description-textfield" label="Description" variant="outlined" value={description} onChange={(e) => setDescription(e.target.value)} size="small" />
                        </FormControl>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DateTimePicker
                                label="Start"
                                value={inputStartDate}
                                onChange={(newValue) => setInputStartDate(newValue)}
                                slotProps={{ textField: { size: 'small' } }} />
                            <DateTimePicker
                                label="End"
                                value={inputEndDate}
                                onChange={(newValue) => setInputEndDate(newValue)}
                                slotProps={{ textField: { size: 'small' } }}
                            />
                        </LocalizationProvider>
                        <Button onClick={handleAddEvent} color="inherit" variant="outlined" sx={{ height: 40 }}>Add Event</Button>
                    </AccordionDetails>
                </Accordion>
                <span>
                    <Button variant="contained" onClick={() => setView("calendar")} sx={{ margin: 1 }}>View Event Calendar</Button>
                    <Button variant="contained" onClick={() => setView("list")} sx={{ margin: 1 }}>View Event List</Button>
                </span>
                <Box
                    component="form"
                    sx={{
                        '& > :not(style)': { m: 1 },
                        display: "flex"
                    }}
                    noValidate
                    autoComplete="off"

                >
                    {view === "calendar" ?
                        <div sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                            <Calendar
                                localizer={localizer}
                                events={filteredEvents}
                                startAccessor="startDate"
                                endAccessor="endDate"
                                style={{
                                    height: 500, width: "98vw", paddingTop: 6, paddingBottom: 6,
                                }}
                                selectable={true}
                                selectedDate={selectedDate}
                                onSelectSlot={(e) => handleSelectedSlot(e)}
                                onSelectEvent={(e) => handleSelectedEvent(e)}
                            />
                            {selectedEvent && <Modal />}
                            {selectedEvents && <MultiEventsModal />}
                        </div>
                        :
                        <List sx={{
                            alignItems: 'center',
                            justifyContent: 'center', width: "94wv"
                        }}>
                            <Typography variant="h4" align="center">
                                Events
                            </Typography>
                            {filteredEvents.map(currentEvent => {
                                return (
                                    <ListItem >
                                        <Accordion>
                                            <AccordionSummary
                                                expandIcon={<ExpandMoreIcon />}
                                                aria-controls="panel1a-content"
                                                id="panel1a-header"
                                                sx={{ display: "flex" }}
                                            >
                                                <Typography align="left" width={"89vw"}><b>Title:</b> {currentEvent.title}</Typography>
                                                <Button align="right" variant="outlined" startIcon={<DeleteIcon />} size="small" onClick={e => handleDelete(e, currentEvent)}>
                                                    <Typography variant="caption">Delete</Typography>
                                                </Button>
                                            </AccordionSummary>
                                            <AccordionDetails>
                                                <div>
                                                    <Typography>
                                                        <b>Description:</b> {currentEvent.description}
                                                    </Typography>
                                                    <Typography>
                                                        <b>Start:</b> {currentEvent.startDate.toDateString()} <b>End:</b> {currentEvent.endDate.toDateString()}
                                                    </Typography>
                                                </div>
                                            </AccordionDetails>
                                        </Accordion>
                                    </ListItem>
                                )
                            })}
                        </List>
                    }
                </Box>
            </Box>

        </Box>
    );
}
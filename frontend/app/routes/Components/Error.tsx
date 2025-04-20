import { isRouteErrorResponse, useRouteError, useParams } from "react-router";
import React from "react";



const Display404 = true

export default function SharedErrorBoundary ({err} : {error: unknown}) {
    const error = useRouteError();
    const params = useParams()
    if (params) return(<h1>Something went wrong when looking for the requested resource {params.id}. Please check your spelling. </h1>)
    if (Display404) return (<h1>Something went wrong D:</h1>)

  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>
          {error.status} {error.statusText}
        </h1>
        <p>{error.data}</p>
      </div>
    );
  } else if (error instanceof Error) {
    return (
      <div>
        <h1>Error</h1>
        <p>{error.message}</p>
        <p>The stack trace is:</p>
        <pre>{error.stack}</pre>
      </div>
    );
  } else {
    return <h1>Unknown Error</h1>;
  }
}
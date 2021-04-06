package weather

import (
	"fmt"

	"github.com/bwmarrin/discordgo"
)

var (
	Commands = []*discordgo.ApplicationCommand{
		{
			Name:        "weather",
			Description: "Weather API command",
			Options: []*discordgo.ApplicationCommandOption{

				// TODO: group passes as a command type
				{
					Type:        discordgo.ApplicationCommandOptionString,
					Name:        "epic",
					Description: "Epic mountains to forecast",
					Choices:     getEpicMountainOptions(),
					Required:    false,
				},

				{
					Type:        discordgo.ApplicationCommandOptionString,
					Name:        "ikon",
					Description: "Ikon mountains to forecast",
					Choices:     getIkonMountainOptions(),
					Required:    false,
				},

				{
					Type:        discordgo.ApplicationCommandOptionInteger,
					Name:        "days-option",
					Description: "Number of days to pull forecasts for",
					Choices: []*discordgo.ApplicationCommandOptionChoice{
						{
							Name:  "1 day",
							Value: 1,
						},
						{
							Name:  "3 day",
							Value: 3,
						},
						{
							Name:  "5 day",
							Value: 5,
						},
						{
							Name:  "10 day",
							Value: 10,
						},
						{
							Name:  "14 day",
							Value: 14,
						},
					},
					Required: false,
				},
			},
		},
		{
			Name:        "responses",
			Description: "Interaction responses",
			Options: []*discordgo.ApplicationCommandOption{
				{
					Name:        "resp-type",
					Description: "Response type",
					Type:        discordgo.ApplicationCommandOptionInteger,
					Choices: []*discordgo.ApplicationCommandOptionChoice{
						{
							Name:  "Acknowledge",
							Value: 2,
						},
						{
							Name:  "Channel message",
							Value: 3,
						},
						{
							Name:  "Channel message with source",
							Value: 4,
						},
						{
							Name:  "Acknowledge with source",
							Value: 5,
						},
					},
					Required: true,
				},
			},
		},
	}

	CommandHandlers = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
		"weather": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			margs := []interface{}{
				i.Data.Options[0].StringValue(),
				i.Data.Options[1].StringValue(),
				i.Data.Options[2].IntValue(),
			}

			msgformat := ` > mountain_option: %s `
			var days int8 = 3

			coordinatesString := i.Data.Options[0].StringValue()

			if len(i.Data.Options) >= 2 {
				msgformat += "\n> days_option: %d"
				coordinatesString = i.Data.Options[1].StringValue()
			}

			if len(i.Data.Options) >= 3 {
				msgformat += "\n> days_option: %d"
				days = int8(i.Data.Options[2].IntValue())
			}

			msg, err := getForecast(coordinatesString, days)

			msgformat += "\n" + msg

			if err != nil {
				panic("Forecast failed")
			}

			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				// Ignore type for now, we'll discuss them in "responses" part
				Type: discordgo.InteractionResponseChannelMessageWithSource,
				Data: &discordgo.InteractionApplicationCommandResponseData{
					Content: fmt.Sprintf(
						msgformat,
						margs...,
					),
				},
			})
		},
		"responses": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			err := s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseType(i.Data.Options[0].IntValue()),
			})
			if err != nil {
				s.FollowupMessageCreate(s.State.User.ID, i.Interaction, true, &discordgo.WebhookParams{
					Content: "Something gone wrong",
				})
			}
		},
	}
)

func getEpicMountainOptions() []*discordgo.ApplicationCommandOptionChoice {

	// TODO TODO TODO TODO TODO TODO TODO !?!!?@!?!?@?!@?!@ pls no
	return []*discordgo.ApplicationCommandOptionChoice{
		{
			Name:  "jfbb",
			Value: "lat=41.109641&lon=-75.652588",
		},
		{
			Name:  "hunter",
			Value: "lat=42.176219&lon=-74.225728",
		},
		{
			Name:  "mt snow",
			Value: "lat=42.959732&lon=-72.924865",
		},
		{
			Name:  "stowe",
			Value: "lat=44.52892&lon=-72.800973",
		},
		{
			Name:  "okemo",
			Value: "lat=43.410329&lon=-72.747451",
		},
		{
			Name:  "jay peak",
			Value: "lat=44.92451&lon=-72.52374",
		},
		{
			Name:  "attitash",
			Value: "lat=44.070258&lon=-71.222398",
		},
		{
			Name:  "crotched",
			Value: "lat=43.005875&lon=-71.879827",
		},
		{
			Name:  "wildcat",
			Value: "lat=44.250096&lon=-71.219147",
		},
		{
			Name:  "mt sunapee",
			Value: "lat=43.321843&lon=-72.071415",
		},
		{
			Name:  "liberty",
			Value: "lat=39.758995&lon=-77.368938",
		},
		{
			Name:  "whitetail",
			Value: "lat=39.742025&lon=-77.935373",
		},
		{
			Name:  "roundtop",
			Value: "lat=40.106815&lon=-76.925932",
		},
		{
			Name:  "breckenridge",
			Value: "lat=39.471854&lon=-106.07911",
		},
		{
			Name:  "keystone",
			Value: "lat=39.579715&lon=-105.9414",
		},
		{
			Name:  "whistler",
			Value: "lat=50.085187&lon=-122.896886",
		},
	}

}

func getIkonMountainOptions() []*discordgo.ApplicationCommandOptionChoice {

	// TODO TODO TODO TODO TODO TODO TODO !?!!?@!?!?@?!@?!@ pls no
	return []*discordgo.ApplicationCommandOptionChoice{
		{
			Name:  "windham",
			Value: "lat=42.288143&lon=-74.255",
		},
		{
			Name:  "stratton",
			Value: "lat=43.100579&lon=-72.918632",
		},
		{
			Name:  "killington",
			Value: "lat=43.617208&lon=-72.797237",
		},
		{
			Name:  "sugarbush",
			Value: "lat=44.13684&lon=-72.900721",
		},
		{
			Name:  "sugarloaf",
			Value: "lat=45.033066&lon=-70.314437",
		},
		{
			Name:  "sunday river",
			Value: "lat=44.457817&lon=-70.868285",
		},
		{
			Name:  "loon",
			Value: "lat=44.036171&lon=-71.624313",
		},
		{
			Name:  "tremblant",
			Value: "lat=46.222045&lon=-74.543412",
		},
		{
			Name:  "revelstoke",
			Value: "lat=51.043257&lon=-118.150182",
		},
		{
			Name:  "cypress",
			Value: "lat=49.407953&lon=-123.194487",
		},
		{
			Name:  "red mountain",
			Value: "lat=49.101402&lon=-117.82593",
		},
		{
			Name:  "squaw",
			Value: "lat=39.181638&lon=-120.27026",
		},
		{
			Name:  "mammoth",
			Value: "lat=37.641989&lon=-119.034776",
		},
		{
			Name:  "crystal",
			Value: "lat=46.926927&lon=-121.505534",
		},
		{
			Name:  "bachelor",
			Value: "43.981695&lon=-121.68624",
		},
		{
			Name:  "steamboat",
			Value: "lat=40.458202&lon=-106.776294",
		},
		{
			Name:  "aspen",
			Value: "lat=39.182382&lon=-106.879125",
		},
		{
			Name:  "copper",
			Value: "lat=39.484704&lon=-106.158884",
		},
		{
			Name:  "winter park",
			Value: "lat=39.874381&lon=-105.773395",
		},
		{
			Name:  "big sky",
			Value: "lat=45.280749&lon=-111.397381",
		},
		{
			Name:  "jackson hole",
			Value: "lat=43.45848&lon=-110.761107",
		},
		{
			Name:  "taos",
			Value: "lat=36.592595&lon=-105.447654",
		},
		{
			Name:  "brighton",
			Value: "lat=40.599588&lon=-111.581664",
		},
		{
			Name:  "alta",
			Value: "lat=40.586266&lon=-111.637529",
		},
		{
			Name:  "snowbird",
			Value: "lat=40.578061&lon=-111.665948",
		},
	}

}

func getForecast(coordinatesString string, days int8) (string, error) {
	return "TODO", nil
}

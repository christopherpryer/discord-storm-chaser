package commands

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

				{
					Type:        discordgo.ApplicationCommandOptionString,
					Name:        "mountain-option",
					Description: "Mountain string to search for",
					Required:    true,
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
				i.Data.Options[1].IntValue(),
			}

			msgformat := ` > mountain_option: %s `
			var days int64 = 3

			if len(i.Data.Options) >= 2 {
				msgformat += "\n> days_option: %d"
				days = i.Data.Options[1].IntValue()
			}

			resort := i.Data.Options[0].StringValue()
			msg, err := getForecast(resort, days)

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

func getForecast(resort string, days int64) (string, error) {
	return "TODO", nil
}
